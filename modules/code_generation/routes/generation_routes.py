import logging
from flask import Blueprint, jsonify, request
from flask_injector import inject
from ..services.ollama_service import OlamaService
from ..services.file_service import FileService
from ..services.command_line_execution_service  import CommandLineExecutionService

from ..repositories.template_repository import TemplateRepository
from ..repositories.technology_repository import TechnologyRepository
from ...project_managment.repositories.project_repository import ProjectRepository
import json
import os
import string

generation_routes = Blueprint('generation', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



@generation_routes.route('/generate-project', methods=['POST'])
@inject
def generate_project(olama_service: OlamaService,
                     file_service: FileService,
                     command_line_service : CommandLineExecutionService,
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

    params_for_actions = {
      "project_name": user_project.name,
      "project_id": user_project.id
    }

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

          stage_actions = json.loads(stage_template.actions)
          
          print(stage_actions)

          if len(stage_actions['actions_before']) > 0 :
            print("We have some actions before generation")
            actions_to_execute = stage_actions['actions_before']

            for action in actions_to_execute :
              formatted_action = command_line_service.format_action(action, params_for_actions)
              output = command_line_service.execute_command(formatted_action)
              print(output)

          if stage_template is None:
              logger.error("Error generating completion: Stage template didn't found")
              return jsonify({"error": "Error generating completion: Stage template didn't found"}), 500


          prompt = stage_template.user_prompt_template.format(
            user_prompt=user_prompt,
            example=stage_template.example,
            template=stage_template.llm_response_template
          )
          
          llm_response = olama_service.generate(prompt,stage_template.llm_response_template)
          
          standard_of_saving_output = json.loads(stage_template.standard_of_saving_output)
          standard_of_saving_output_type = standard_of_saving_output['type']

          if standard_of_saving_output_type == "one_file" :
            filename = standard_of_saving_output['filename']
            user_project_path = f"./generated_projects/{user_project.id}"
            file_service.create_folder(user_project_path)
            file_service.create_file(filename,llm_response,user_project_path)

          elif standard_of_saving_output == "many_files" :
            print("Save many file inside the project")

          if len(stage_actions['actions_after']) > 0 :
            print("We have some actions after generation")
            actions_to_execute = stage_actions['actions_after']

            for action in actions_to_execute :
              outupt = command_line_service.execute_command(action)
              print(outupt)

          loop_stage+=1
        
        return jsonify({"response": "ok"}), 200

    except Exception as e:
        logger.error(f"Error generating completion: {str(e)}")
        return jsonify({"error": "Failed to generate project"}), 500
