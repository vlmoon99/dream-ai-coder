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
    data = request.get_json()
    template = TemplateModel(
        technology=data['technology'],
        author=data['author'],
        stage=data['stage'],
        template=data['template'],
        example=data['example'],
        description=data['description']
    )
    created_template = template_repository.create(template)
    return jsonify(created_template.to_dict()), 201


@template_routes.route('/templates/<string:template_id>', methods=['GET'])
@inject
def get_template(template_id, template_repository: TemplateRepository):
    template = template_repository.get_by_id(template_id)
    if template:
        return jsonify(template.to_dict()), 200
    return jsonify({"error": "Template not found"}), 404


@template_routes.route('/templates/<string:template_id>', methods=['PUT'])
@inject
def update_template(template_id, template_repository: TemplateRepository):
    data = request.get_json()
    current_template = template_repository.get_by_id(template_id)
    if not current_template:
        return jsonify({"error": "Template not found"}), 404

    updated_template = TemplateModel(
        _id=current_template.id,
        technology=data.get("technology", current_template.technology),
        stage=data.get("stage", current_template.stage),
        template=data.get("template", current_template.template),
        example=data.get("example", current_template.example),
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
    deleted = template_repository.delete(template_id)
    if deleted:
        return jsonify({"message": "Template deleted successfully"}), 200
    return jsonify({"error": "Template not found"}), 404
