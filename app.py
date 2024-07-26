from models.environment import Environment
from models.user_requirements import UserRequirements
from models.business_requirements import BusinessRequirements

from models.template import Template, TemplateStage
from models.project import Project

def main():
    print("Welcome to the AI Coder Machine Console App!")

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
            TemplateStage(name="Create Domain Models", description="Create entities and relationships."),
            TemplateStage(name="Define UI Screens", description="Define the user interface."),
            TemplateStage(name="Final Testing", description="Test the application."),
        ]
    elif selected_environment == Environment.JAVA_SPRING:
        stages = [
            TemplateStage(name="Setup Project Structure", description="Setup the project structure."),
            TemplateStage(name="Implement Business Logic", description="Implement core business logic."),
            TemplateStage(name="Final Testing", description="Test the application."),
        ]
    else:
        print("Environment not supported!")
        return

    # Create a template for the project
    template = Template(
        name=f"{selected_environment.value} Template",
        environment=selected_environment,
        stages=stages
    )

    # Get user requirements
    user_description = input("Describe the project requirements: ")
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
            print(f"Current Stage: {next_stage.name} - {next_stage.description}")
            input("Press Enter to complete the current stage...")  # Simulate user approval
            print(project.proceed_to_next_stage())
        else:
            print("Project setup completed successfully!")
            break

if __name__ == "__main__":
    main()
