# routes.py

from flask import Blueprint, jsonify, render_template
from flask_injector import inject

# Import your services
from services.ai_generation_service import AIGenerationService

# Create a Blueprint for the routes
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

# Add more routes as needed
@bp.route('/generate', methods=['GET'])
@inject
def generate_code(ai_generation_service: AIGenerationService):
    # Logic to generate code using ai_generation_service
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

    
    response = ai_generation_service.generate_code(prompt = prompt_template)
    dart_code = ai_generation_service.extract_dart_code(response = response)

    print("Extracted Dart Code:\n")
    print(dart_code)
    file_path = "/home/mit-pc/Documents/work/deeplearning/practice/dream-ai-coder/flutter_project_for_generation/lib/models"
    file_name = "user_model.dart"   
    full_path = f"{file_path}/{file_name}"

    with open(full_path, "w") as file:
        file.write(dart_code)


    return jsonify(dart_code)
