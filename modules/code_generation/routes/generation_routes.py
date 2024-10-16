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
import glob

generation_routes = Blueprint('generation', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



def get_context_for_one_file_generation(stage_template, user_project_path, command_line_service, params_for_actions):
    file_contents = []
    context = ''
    if stage_template.context is not None :
      filenames = json.loads(stage_template.context)
    
      separator = "\n---\n"
      file_contents = []
    
      if os.path.exists(user_project_path) and os.path.isdir(user_project_path):
          for filename in filenames:
    
            if len(filename.split("/")) > 1 :
              if filename.endswith("*") :
                formatted_filename_path = command_line_service.format_action(filename, params_for_actions)
                print("FormatedPath")
                print(formatted_filename_path)
                with open(os.path.join(user_project_path, formatted_filename_path), 'r') as file:
                  file_contents.append(file.read())
    
            else :
              with open(os.path.join(user_project_path, filename), 'r') as file:
                file_contents.append(file.read())
    
    context = separator.join(file_contents) if file_contents else "No context"
    
    return context


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

    user_project_path = f"./generated_projects/{user_project.id}/"
    user_project_app_path = f"./generated_projects/{user_project.id}/{user_project.name}/"

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
          
          standard_of_saving_output = json.loads(stage_template.standard_of_saving_output)
          standard_of_saving_output_type = standard_of_saving_output['type']


          stage_actions = {"actions_before" : [], "actions_after" : [] }
          if isinstance(stage_template.actions, str):
              stage_actions = json.loads(stage_template.actions)
          else:
              stage_actions = stage_template.actions

          
          if len(stage_actions['actions_before']) > 0 :
            actions_to_execute = stage_actions['actions_before']

            for action in actions_to_execute :
              formatted_action_before = command_line_service.format_action(action, params_for_actions)
              output = command_line_service.execute_command(formatted_action_before)

          if stage_template is None:
              logger.error("Error generating completion: Stage template didn't found")
              return jsonify({"error": "Error generating completion: Stage template didn't found"}), 500

          llm_response = []


          if standard_of_saving_output_type == "many_files" :
            context_files = json.loads(stage_template.context)
            context_files = [file_path.replace("{project_name}", user_project.name) for file_path in context_files]

            filename = context_files[0]
            parsed_structure = []
            
            additional_context_files = context_files[:1]
            expanded_files = []
            for file in additional_context_files:
                if '*' in file:
                    for expanded_file in glob.glob(file):
                        try:
                            with open(expanded_file, 'r') as f:
                                content = f.read()
                                expanded_files.append(f"Path: {expanded_file}\nContent:\n{content}\n")
                        except Exception as e:
                            print(f"Error reading file {expanded_file}: {e}")
                else:
                    try:
                        with open(file, 'r') as f:
                            content = f.read()
                            expanded_files.append(f"Path: {file}\nContent:\n{content}\n")
                    except Exception as e:
                        print(f"Error reading file {file}: {e}")

            concatenated_context = '\n'.join(expanded_files)

            print(f"Structured Concatenated Context:\n{concatenated_context}")

            
            with open(os.path.join(user_project_path, filename), 'r') as file:
              parsed_structure = json.loads(file.read())

            print(f"parsed_structure {parsed_structure}")
            
            for entry in parsed_structure :
              prompt = stage_template.user_prompt_template.format(
              user_prompt="Generate me data by provided template using provided data in the context",
              example=stage_template.example,
              template=stage_template.llm_response_template,
              context=entry)
              response = olama_service.generate(prompt,stage_template.llm_response_template)
              llm_response.append(response[0])

          elif standard_of_saving_output_type == "one_file" :
            context = get_context_for_one_file_generation(stage_template, user_project_path, command_line_service, params_for_actions)

            prompt = stage_template.user_prompt_template.format(
              user_prompt=user_prompt,
              example=stage_template.example,
              template=stage_template.llm_response_template,
              context=context)
            llm_response = olama_service.generate(prompt,stage_template.llm_response_template)


          if standard_of_saving_output_type == "one_file" :
            filename = standard_of_saving_output['filename']
            file_service.create_folder(user_project_path)
            encoded_response = json.dumps(llm_response, ensure_ascii=False)
            file_service.create_file(filename,encoded_response,user_project_path)

          elif standard_of_saving_output_type == "many_files" :
            template = standard_of_saving_output['filename']

            print(f"TEMPLATE ::: {template}")
            print(f"llm_response ::: {llm_response}")
          
            for response in llm_response :
              filename = response['filename']
              content = response['content']
              formatted_stage_path = command_line_service.format_action(stage_template.project_folder, params_for_actions)
              full_path = f"{user_project_path}{formatted_stage_path}"
              file_service.create_folder(full_path)
              file_service.create_file(filename,content,full_path)


          if len(stage_actions['actions_after']) > 0 :
            actions_to_execute = stage_actions['actions_after']

            for action in actions_to_execute :
              formatted_action_after = command_line_service.format_action(action, params_for_actions)
              print(formatted_action_after)
              output = command_line_service.execute_command(formatted_action_after)


          loop_stage+=1
          user_project.current_stage += 1
          project_repository.update(user_project.id,user_project)


        
        return jsonify({"response": "ok"}), 200

    except Exception as e:
        logger.error(f"Error generating completion: {str(e)}")
        return jsonify({"error": "Failed to generate project"}), 500
