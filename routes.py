# routes.py

from flask import Blueprint, jsonify, render_template, request
from flask_injector import inject

# Import your services
from services.ai_generation_service import AIGenerationService

# Create a Blueprint for the routes
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/generate-structured-business-requirement', methods=['POST'])
def generate_structured_business_requirement(ai_generation_service: AIGenerationService):
    user_input = None
    
    data = request.get_json()
    if data and 'user_input' in data:
        user_input = data['user_input']
        # prompt_template = r"""                
        #     {{
        #     "system": [{{"system_context" : "You are the code-generator."}},],
        #     "user": [{{"data_request": ""}},],            
        #     "assistant": [{{"response" : [{"generated_business_requirements" : ""},],}}]
        #     }}
        #     """
        prompt_template = r"""                
            {{

            "system": [{{"system_context" : 
            "
            You are the structured business requirements generator.
            You generate domain entities and use cases from user input which will be unique each time.
            Use provided template for business requirement : 
            
            //////Template//////
            {
            "user_input" : "user_input"
            "generated_entities" : [],
            "generated_use_cases" : [],
            }
            //////Template//////

            "

            }},],

            "user": [{{"data_request": "
            Business Requirements for a Multi-Platform To-Do Application

            **Business Overview:**

            Our company, TaskFlow Solutions, aims to develop a multi-platform To-Do application that will enhance productivity and task management for individuals and teams. The app should be intuitive, accessible. The primary goal is to help users efficiently organize tasks, set priorities, and collaborate with team members.

            **Target Audience:**

            - **Individuals** who need to manage personal tasks and deadlines.
            - **Teams** requiring collaboration tools for project management.
            - **Small to medium-sized businesses** seeking an affordable task management solution.

            **Functional Requirements:**

            1. **User Registration and Authentication:**
            - Users should be able to register using email, Google, or social media accounts.
            - Implement secure login and authentication processes, including password recovery.

            2. **Task Management:**
            - Users can create, edit, delete, and organize tasks.
            - Ability to set deadlines and priorities for each task.
            - Support for recurring tasks (e.g., daily, weekly).

            3. **Task Categorization and Tagging:**
            - Users can categorize tasks using custom labels or tags.
            - Implement filters to sort tasks by category, due date, or priority.

            4. **Collaboration Features:**
            - Allow users to share tasks or projects with others.
            - Implement real-time collaboration with multiple users editing tasks simultaneously.
            - Provide comments and discussion threads for each task.

            5. **Notifications and Reminders:**
            - Push notifications and email reminders for upcoming deadlines and task updates.
            - Customizable reminder settings for different tasks.

            6. **Cross-Platform Synchronization:**
            - Real-time data synchronization across all devices and platforms.
            - Offline access to tasks with automatic syncing when online.

            7. **Search Functionality:**
            - Implement a search bar to find tasks quickly using keywords or filters.
            - Support for advanced search queries (e.g., tasks due next week).

            8. **Dashboard and Analytics:**
            - Provide a dashboard with an overview of pending tasks, deadlines, and progress.
            - Generate reports on productivity metrics and task completion rates.

            9. **Integration with Third-Party Services:**
            - Integrate with calendars (e.g., Google Calendar, Outlook) for seamless scheduling.
            - Support integration with popular productivity tools like Slack and Trello.

            10. **Settings and Preferences:**
                - Allow users to customize app themes and interface settings.
                - Provide language support for a global user base.


            **Use Cases:**

            1. **Create a New Task:**
            - **Actors:** Individual User
            - **Preconditions:** User is logged in.
            - **Steps:**
                1. Navigate to the "Add Task" screen.
                2. Enter task details (title, description, due date, priority).
                3. Save the task.
            - **Postconditions:** Task is added to the user's task list.

            2. **Collaborate on a Task:**
            - **Actors:** Team Member, Collaborator
            - **Preconditions:** User has shared access to the task.
            - **Steps:**
                1. Open a shared task.
                2. Add comments or make edits.
                3. Notify other collaborators of changes.
            - **Postconditions:** Task updates are visible to all collaborators.

            3. **Receive Task Reminder:**
            - **Actors:** Individual User
            - **Preconditions:** User has set a reminder for a task.
            - **Steps:**
                1. Reminder notification is triggered.
                2. User views the reminder.
                3. Optionally, user snoozes or dismisses the reminder.
            - **Postconditions:** User is notified of the task deadline.

            4. **Sync Tasks Across Devices:**
            - **Actors:** Individual User
            - **Preconditions:** User is logged in on multiple devices.
            - **Steps:**
                1. Add or update a task on one device.
                2. Sync task data to the server.
                3. Access the app on another device.
                4. Verify that task changes are reflected.
            - **Postconditions:** Task data is consistent across all devices.
            "}},],            
            "assistant": [{{"response" : [{"generated_business_requirements" : " Based on your prompt I generetade next structure :
            
            """

        ai_generation_service.generate_text_from_prompt(prompt=prompt_template)

    else:
        return jsonify({"error": "Missing 'user_input' parameter in the request body"}), 400


    return jsonify({"user_input": user_input})


@bp.route('/test-generate', methods=['GET'])
@inject
def generate_code(ai_generation_service: AIGenerationService):
    prompt_template = r"""
            [
            
                {{
                    "system": ["system_context" : "You are the code-generator. You generate entities by provided requirements + provided template qithout using any additional packages and annotations"],
                    "user": "[{{\"data_request\":\"Create Dart class from this template --> [

                import 'package:json_annotation/json_annotation.dart';
                part 'model_name.g.dart';

                @JsonSerializable()
                class ModelName {

                final <T> model_property_name;

                ModelName({
                    required this.model_property_name,
                });

                factory ModelName.fromJson(Map<String, dynamic> json) =>
                    _$ModelNameFromJson(json);

                Map<String, dynamic> toJson() => _$ModelNameFromJson(this);

                ModelName copyWith({
                    T? model_property_name,
                }) {
                    return ModelName(
                    model_property_name: model_property_name ?? this.model_property_name,
                    );
                }
                
                } 
            ]\ ,
            using this business requirements -- >  Create Dart class with name : User , and fileds [id : String , createdAt : Date,updatedAt : Date, age : int,], file_name must be user_model.dart, pls take it into account"}}]",
            }}
            ],
            "assistant": ["response" : [{"file_name" : "{class_name_model}.dart","file_data":"
            
                            import 'package:json_annotation/json_annotation.dart';
                part 'model_name.g.dart';

                @JsonSerializable()
                class ModelName {

                final <T> model_property_name;

                ModelName({
                    required this.model_property_name,
                });

                factory ModelName.fromJson(Map<String, dynamic> json) =>
                    _$ModelNameFromJson(json);

                Map<String, dynamic> toJson() => _$ModelNameFromJson(this);

                ModelName copyWith({
                    T? model_property_name,
                }) {
                    return ModelName(
                    model_property_name: model_property_name ?? this.model_property_name,
                    );
                }
                
                } 
            
            "},]]
            """

    
    response = ai_generation_service.generate_text_from_prompt(prompt = prompt_template)
    dart_code = ai_generation_service.extract_dart_code(response = response)

    print("Extracted Dart Code:\n")
    print(dart_code)
    file_path = "/home/mit-pc/Documents/work/deeplearning/practice/dream-ai-coder/flutter_project_for_generation/lib/models"
    file_name = "user_model.dart"   
    full_path = f"{file_path}/{file_name}"

    with open(full_path, "w") as file:
        file.write(dart_code)


    return jsonify(dart_code)
