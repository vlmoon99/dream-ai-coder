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
            prompt_template="""
            1. Filename: user.dart
            import 'package:json_annotation/json_annotation.dart';

            part 'user.g.dart';

            @JsonSerializable()
            class User {
                final int id;
                final String name;
                final String email;

                User({
                    required this.id,
                    required this.name,
                    required this.email,
                });

                factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);

                Map<String, dynamic> toJson() => _$UserToJson(this);
            }
            2. Filename: product.dart
            import 'package:json_annotation/json_annotation.dart';

            part 'product.g.dart';

            @JsonSerializable()
            class Product {
                final int id;
                final String name;
                final double price;

                Product({
                    required this.id,
                    required this.name,
                    required this.price,
                });

                factory Product.fromJson(Map<String, dynamic> json) => _$ProductFromJson(json);

                Map<String, dynamic> toJson() => _$ProductToJson(this);
            }
            3. Filename: order.dart
            import 'package:json_annotation/json_annotation.dart';

            part 'order.g.dart';

            @JsonSerializable()
            class Order {
                final int id;
                final int userId;
                final List<int> productIds;

                Order({
                    required this.id,
                    required this.userId,
                    required this.productIds,
                });

                factory Order.fromJson(Map<String, dynamic> json) => _$OrderFromJson(json);

                Map<String, dynamic> toJson() => _$OrderToJson(this);
            }
            """,
            system_prompt="""
            You are the code-generator, you generate entity models by provided templates using business requirements
            """
            ),
            TemplateStage(name="Define UI Screens", description="Define the user interface.",
            prompt_template = 
            """
            """,
            system_prompt=
            """
            You are the code-generator , you generate modules,pages,vms,services,repositories,models by provided tempaltes using buinsess requirements
            """
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
            if next_stage is not None and next_stage.system_prompt is not None and next_stage.prompt_template is not None :
                ai_generation_service.generateCode(system_prompt= next_stage.system_prompt,prompt_template= next_stage.prompt_template,busines_requirements=project.business_requirements)

            print(f"Current Stage: {next_stage.name} - {next_stage.description}")
            input("Press Enter to complete the current stage...")  # Simulate user approval
            print(project.proceed_to_next_stage())
        else:
            print("Project setup completed successfully!")
            break

if __name__ == "__main__":
    main()
