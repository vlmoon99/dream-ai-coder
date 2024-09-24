import logging
from flask import Blueprint, jsonify, request
from flask_injector import inject
from ..repositories.template_repository import TemplateRepository
from ..models.template_model import TemplateModel
from datetime import datetime

template_routes = Blueprint('template', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@template_routes.route('/create-template', methods=['POST'])
@inject
def create_template(template_repository: TemplateRepository):
    """
    Create a new template.
    ---
    tags:
      - Template
    parameters:
      - name: template
        in: body
        required: true
        schema:
          type: object
          properties:
            technology:
              type: string
            author:
              type: string
            stage:
              type: integer
            llm_response_template:
              type: string
            user_prompt_template:
              type: string
            example:
              type: string
            description:
              type: string
    responses:
      201:
        description: Template created successfully
        schema:
          type: object
          properties:
            id:
              type: string
            technology:
              type: string
            author:
              type: string
            stage:
              type: integer
            llm_response_template:
              type: string
            user_prompt_template:
              type: string
            example:
              type: string
            description:
              type: string
      400:
        description: Invalid input
    """
    data = request.get_json()
    template = TemplateModel(
        technology=data['technology'],
        author=data['author'],
        stage=data['stage'],
        llm_response_template=data['llm_response_template'],
        user_prompt_template=data['user_prompt_template'],
        example=data['example'],
        description=data['description']
    )
    created_template = template_repository.create(template)
    return jsonify(created_template.to_dict()), 201


@template_routes.route('/templates/<string:template_id>', methods=['GET'])
@inject
def get_template(template_id, template_repository: TemplateRepository):
    """
    Get a template by ID.
    ---
    tags:
      - Template
    parameters:
      - name: template_id
        in: path
        required: true
        type: string
    responses:
      200:
        description: Template retrieved successfully
        schema:
          type: object
          properties:
            id:
              type: string
            technology:
              type: string
            author:
              type: string
            stage:
              type: integer
            llm_response_template:
              type: string
            user_prompt_template:
              type: string
            example:
              type: string
            description:
              type: string
      404:
        description: Template not found
    """
    template = template_repository.get_by_id(template_id)
    if template:
        return jsonify(template.to_dict()), 200
    return jsonify({"error": "Template not found"}), 404


@template_routes.route('/templates/<string:template_id>', methods=['PUT'])
@inject
def update_template(template_id, template_repository: TemplateRepository):
    """
    Update an existing template by ID.
    ---
    tags:
      - Template
    parameters:
      - name: template_id
        in: path
        required: true
        type: string
      - name: template
        in: body
        required: false
        schema:
          type: object
          properties:
            technology:
              type: string
            author:
              type: string
            stage:
              type: integer
            llm_response_template:
              type: string
            user_prompt_template:
              type: string
            example:
              type: string
            description:
              type: string
            standard_of_saving_output:  # Add this field to the Swagger docs
              type: string
    responses:
      200:
        description: Template updated successfully
      404:
        description: Template not found
      400:
        description: Update failed
    """
    data = request.get_json()
    current_template = template_repository.get_by_id(template_id)
    if not current_template:
        return jsonify({"error": "Template not found"}), 404


    # template_content = (
    #     "This is the template by which you will generate code ---> : {template} "
    #     "This is the example of how to write response ---> : {example} "
    #     "This is the requirements of the response ---> : It must contain a list of entities in JSON format like this one: [first_entity, second_entity, ...], "
    #     "This is the prompt ---> : {user_prompt}"
    # )

    updated_template = TemplateModel(
        _id=current_template.id,
        technology=data.get("technology", current_template.technology),
        author=data.get("author", current_template.author),
        stage=data.get("stage", current_template.stage),
        llm_response_template=data.get("llm_response_template", current_template.llm_response_template),
        user_prompt_template=data.get("user_prompt_template", current_template.user_prompt_template),
        example=data.get("example", current_template.example),
        description=data.get("description", current_template.description),
        standard_of_saving_output=data.get("standard_of_saving_output", current_template.standard_of_saving_output),  # Handle the new field
        created_at=current_template.created_at,
        updated_at=datetime.utcnow()
    )

    updated = template_repository.update(template_id, updated_template)
    if updated:
        return jsonify({"message": "Template updated successfully"}), 200
    return jsonify({"error": "Update failed"}), 400


@template_routes.route('/templates/<string:template_id>', methods=['DELETE'])
@inject
def delete_template(template_id, template_repository: TemplateRepository):
    """
    Delete a template by ID.
    ---
    tags:
      - Template
    parameters:
      - name: template_id
        in: path
        required: true
        type: string
    responses:
      200:
        description: Template deleted successfully
      404:
        description: Template not found
    """
    deleted = template_repository.delete(template_id)
    if deleted:
        return jsonify({"message": "Template deleted successfully"}), 200
    return jsonify({"error": "Template not found"}), 404
