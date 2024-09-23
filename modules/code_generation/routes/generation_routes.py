import logging
from flask import Blueprint, jsonify, request
from flask_injector import inject
from ..services.ollama_service import OlamaService
from ..repositories.template_repository import TemplateRepository
from ...project_managment.repositories.project_repository import ProjectRepository
import json

generation_routes = Blueprint('generation', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@generation_routes.route('/generate-project', methods=['POST'])
@inject
def generate_project(olama_service : OlamaService,
                     project_repository : ProjectRepository, 
                     template_repository : TemplateRepository):
    data = request.get_json()
    prompt = data.get('prompt')
    project_id = data.get('project_id')

    user_project = project_repository.get_by_id(project_id=project_id)
    
    if user_project is None :
        logger.error("Error generating completion: User project didn't found")
        return jsonify({"error": "Failed to generate completion"}), 500

    
    stage_template = template_repository.get_template_by_tech_and_author(
        user_project.technology, "root", user_project.current_stage)
    
    if stage_template is None:
        logger.error("Error generating completion: Stage tempalte didn't found")
        return jsonify({"error": "Failed to generate completion"}), 500

    try:
        completion = olama_service.generate(
            prompt, stage_template.template, stage_template.example)
        response_str = completion.get("response", "")
        print(response_str)
        response_json = json.loads(response_str)
        print(response_json)
        # prettified_response = json.dumps(response_json, indent=3)
        # print(prettified_response)
        return jsonify({"response": response_json}), 200
    except Exception as e:
        logger.error(f"Error generating completion: {str(e)}")
        return jsonify({"error": "Failed to generate completion"}), 500
