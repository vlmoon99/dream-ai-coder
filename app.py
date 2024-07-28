from models.environment import Environment
from models.user_requirements import UserRequirements
from models.business_requirements import BusinessRequirements

from models.template import Template, TemplateStage
from models.project import Project
from services.ai_generation_service import AIGenerationService

def main():
    print("Welcome to the AI Coder Machine Console App!")
    ai_generation_service = AIGenerationService()
    # Get user input for project setup
    project_name = input("Enter the project name: ")
    project_path = input("Enter the project full pwd path: ")

    # Choose environment
    print("Select the development environment:")
    environments = list(Environment)
    for idx, env in enumerate(environments):
        print(f"{idx + 1}. {env.value}")
    
    env_choice = int(input("Enter the number corresponding to your choice: ")) - 1
    selected_environment = environments[env_choice]

    # Define template stages for the chosen environment
    if selected_environment == Environment.FLUTTER_DART:
        stages = [
            TemplateStage(
            name="Create Domain Models",
            description="Create entities and relationships.",
     
            ),
            TemplateStage(name="Define UI Screens", description="Define the user interface.",
                        # prompt_template = 

            prompt_template = r"""
            [
            
                {{
                    "system": "You are the code-generator. You generate entities by provided requirements",
                    "user": "[{{\"data_request\":\"Create Dart class with name {class_name} and fields [{fields}], from this template --> [

            import 'package:json_annotation/json_annotation.dart';
            part '{file_name}.g.dart';

            @JsonSerializable()
            class {class_name} {{

                {properties}

                {constructor}

                factory {class_name}.fromJson(Map<String, dynamic> json) =>
                    _${class_name}FromJson(json);

                Map<String, dynamic> toJson() => _${class_name}ToJson(this);

                {copy_with}
                
            }}
            ]\"}}]",
                    "assistant": "[]",
                }}
            ]
            """,
            ),
            TemplateStage(name="Final Testing", description="Test the application.",system_prompt= None),
        ]
    elif selected_environment == Environment.JAVA_SPRING:
        stages = [
            TemplateStage(name="Setup Project Structure", description="Setup the project structure.",system_prompt= ""),
            TemplateStage(name="Implement Business Logic", description="Implement core business logic.",system_prompt= ""),
            TemplateStage(name="Final Testing", description="Test the application.",system_prompt= None),
        ]
    else:
        print("Environment not supported!")
        return

    template = Template(
        name=f"{selected_environment.value} Template",
        environment=selected_environment,
        stages=stages
    )

    # Get user requirements
    user_description = "Create the Blog post app , wherein users will crud posts and display it on the main screen, it msut be simple concep app without any complex logic"
    user_requirements = UserRequirements(user_description)

    business_requirements = BusinessRequirements(user_requirements)

    # Initialize the project
    project = Project(
        name=project_name,
        path=project_path,
        template=template,
        business_requirements=business_requirements
    )

    # Output project details
    print(f"Project '{project.name}' created at {project.path}")

    # Proceed through the stages
    while True:
        next_stage = project.template.get_next_stage()
        if next_stage:
            if next_stage is not None :
                generation_request =  ai_generation_service.generateCode(system_prompt= next_stage.system_prompt,prompt_template= next_stage.prompt_template,busines_requirements=project.business_requirements)
                print(generation_request)

            print(f"Current Stage: {next_stage.name} - {next_stage.description}")
            input("Press Enter to complete the current stage...")  # Simulate user approval
            print(project.proceed_to_next_stage())
        else:
            print("Project setup completed successfully!")
            break

if __name__ == "__main__":
    main()
