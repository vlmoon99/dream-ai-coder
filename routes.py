# routes.py

from flask import Blueprint, jsonify
from flask_injector import inject

# Import your services
from services.ai_generation_service import AIGenerationService

# Create a Blueprint for the routes
bp = Blueprint('main', __name__)

# Example route using dependency injection
@bp.route('/')
@inject
def index():
    return jsonify({
        "message": "Welcome to the AI Coder Machine Console App!",
        "status": "success"
    })

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
            using this business requirements -- >  Create Dart class with name : User , and fileds [id : String , createdAt : Date,updatedAt : Date, age : int,]"}}]",
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

    
    result = ai_generation_service.generateCode(prompt = prompt_template)

    return jsonify(result)
