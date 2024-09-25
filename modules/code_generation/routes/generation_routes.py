import logging
from flask import Blueprint, jsonify, request
from flask_injector import inject
from ..services.ollama_service import OlamaService
from ..repositories.template_repository import TemplateRepository
from ..repositories.technology_repository import TechnologyRepository
from ...project_managment.repositories.project_repository import ProjectRepository
import json

generation_routes = Blueprint('generation', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def extract_keys_from_json(json_obj):
    """
    Recursively extract all keys from a nested dictionary structure.
    """
    keys = set()
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            keys.add(key)
            if isinstance(value, dict):
                keys.update(extract_keys_from_json(value))
    return keys

def compare_keys(template_keys, response_keys):
    """
    Compare the keys from the template and the response.
    """
    return template_keys == response_keys


@generation_routes.route('/generate-project', methods=['POST'])
@inject
def generate_project(olama_service: OlamaService,
                     project_repository: ProjectRepository,
                     technology_repository: TechnologyRepository,
                     template_repository: TemplateRepository):
    """
    Generate a project based on a prompt and project ID.
    ---
    tags:
      - Generation
    parameters:
      - name: generation
        in: body
        required: true
        schema:
          type: object
          properties:
            prompt:
              type: string
              description: The prompt to generate the project.
            project_id:
              type: string
              description: The ID of the project to generate.

    responses:
      200:
        description: Project generated successfully
        schema:
          type: object
          properties:
            response:
              type: object
      400:
        description: Invalid input
      404:
        description: Project not found
      500:
        description: Failed to generate completion
    """
    data = request.get_json()
    user_prompt = data.get('prompt')
    project_id = data.get('project_id')

    user_project = project_repository.get_by_id(project_id=project_id)

    if user_project is None:
        logger.error("Error generating completion: User project didn't found")
        return jsonify({"error": "Error generating completion: User project didn't found"}), 500

    project_technology = technology_repository.get_by_technology(user_project.technology)

    if project_technology is None :
        logger.error(
            "Error generating completion: Project Technology didn't found")
        return jsonify({"error": "Error generating completion: Project Technology didn't found"}), 500
    
    loop_stage = user_project.current_stage

    try:
        logger.info(f"Start Generation on : {user_project.name} Project")

        while loop_stage < project_technology.stages + 1 :
          logger.info(f"Start generate process of stage {loop_stage}")

          stage_template = template_repository.get_template_by_tech_and_author(user_project.technology, "root", loop_stage)

          if stage_template is None:
              logger.error("Error generating completion: Stage template didn't found")
              return jsonify({"error": "Error generating completion: Stage template didn't found"}), 500


          prompt = stage_template.user_prompt_template.format(
            user_prompt=user_prompt,
            example=stage_template.example,
            template=stage_template.llm_response_template
          )
          
          template_keys = extract_keys_from_json(json.loads(stage_template.llm_response_template))

          print(template_keys)

          llm_response = None

          for attempt in range(5):
              llm_response = olama_service.generate(prompt)

              print(llm_response)

              response_keys = extract_keys_from_json(llm_response)
              
              if compare_keys(template_keys, response_keys):
                  print(f"Valid response on attempt {attempt + 1}")
                  break
              else:
                  print(f"Attempt {attempt + 1}: Invalid response structure. Expected keys: {template_keys}, but got: {response_keys}")

          if llm_response is None :
            raise Exception(f"Failed to generate valid response after {max_retries} attempts.")

          next_generation_task_in_current_stage = llm_response.get("next_generation_task",[])

          if len(next_generation_task_in_current_stage) != 0 :
            print("We have more task to generate")
            
          else :
            print("We finish generation process")


          # standard_of_saving_output = json.loads(stage_template.standard_of_saving_output)
          # standard_of_saving_output_type = parsed_data['type']
          # filename = parsed_data['filename']

          loop_stage+=1
        
        return jsonify({"response": "ok"}), 200

    except Exception as e:
        logger.error(f"Error generating completion: {str(e)}")
        return jsonify({"error": "Failed to generate project"}), 500
