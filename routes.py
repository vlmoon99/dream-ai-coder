import logging

from flask import Blueprint, jsonify, render_template, request, Response
from flask_injector import inject


# Import your services
from services.ai_generation_service import AIGenerationService
from services.video_streaming_service import VideoStreamingService

# Create a Blueprint for the routes
bp = Blueprint('main', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/capture_screenshot', methods=['GET'])
def capture_screenshot(video_service: VideoStreamingService):
    screenshot_base64 = video_service.capture_screenshot()
    if screenshot_base64:
        return jsonify({'screenshot': screenshot_base64})
    else:
        return jsonify({'error': 'Failed to capture screenshot'}), 500



@bp.route('/generate-structured-business-requirement', methods=['GET'])
def generate_structured_business_requirement(ai_generation_service: AIGenerationService):
    user_input = None
    
    # data = request.get_json()
    # if data and 'user_input' in data:
    #     user_input = data['user_input']
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
            You generate domain entities from user input which will be unique each time.
            Use provided template for your response : 
            
            //////Template//////
            Use this template for your response, it must contain dict entry with key generated_entities and value as list.
            VERY IMPORTANT : You have only a few available entity_type basic types (We dont take created Entities as type) , its : Integer,Double,String.Boolean
            {
               "generated_entities" : [
                    {
                    "entity_name" : "entity_name",
                    "entity_properties" : [{"entity_property_name" : "entity_type",} + (n + 1)]
                    "entity_file_name" : "entity_model.dart"
                    },
                ],
                "generation"
            }
            //////Template//////

            "

            }},],

            "user": [{{"data_request": "

            **To-Do App Requirements**

                    **Overview:**

                    Make a task app.

                    **Audience:**

                    - Only 1 client can use this app.

                    **Requirements:**

                    1. **Accounts:**
                    - Headlesss Register.

                    2. **Tasks:**
                    - Make tasks.

                    3. **Tags:**
                    - Organize.

                    4. **Share:**
                    - Share tasks.

                    5. **Reminders:**
                    - Get alerts.


                    **Use Cases:**

                    1. **Add Task:**
                    - Add it.

                    2. **Share Task:**
                    - Share it.

                    3. **Remind:**
                    - Get alerted.

            "}},],            
            "assistant": [{{"response" : [{"generated_business_requirements" : " Based on your prompt I generetade next structure :
            {
            "generated_entities" : [
                    {
                    "entity_name" : "entity_name",
                    "entity_properties" : [{"entity_property_name" : "entity_type",} + (n + 1)]
                    "entity_file_name" : "entity_model.dart"
                    },
                ],
            }            
            """

    result = ai_generation_service.generate_text_from_prompt(prompt=prompt_template)
    print(result)
    return jsonify({"result": ai_generation_service.parse_generated_entities(result)})

    # else:
    #     return jsonify({"error": "Missing 'user_input' parameter in the request body"}), 400

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
