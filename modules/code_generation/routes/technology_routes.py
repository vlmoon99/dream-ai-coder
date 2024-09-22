import logging
from flask import Blueprint, jsonify, request
from flask_injector import inject
from ..repositories.technology_repository import TechnologyRepository
from ..models.technology_model import TechnologyModel
from datetime import datetime

technology_routes = Blueprint('technology', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@technology_routes.route('/create-technology', methods=['POST'])
@inject
def create_technology(technology_repository: TechnologyRepository):
    data = request.get_json()
    technology = TechnologyModel(
        technology=data['technology'],
        stages=data['stages']
    )
    created_technology = technology_repository.create(technology)
    return jsonify(created_technology.to_dict()), 201


@technology_routes.route('/technologies/<string:technology_id>', methods=['GET'])
@inject
def get_technology(technology_id, technology_repository: TechnologyRepository):
    technology = technology_repository.get_by_id(technology_id)
    if technology:
        return jsonify(technology.to_dict()), 200
    return jsonify({"error": "Technology not found"}), 404


@technology_routes.route('/technologies/<string:technology_id>', methods=['PUT'])
@inject
def update_technology(technology_id, technology_repository: TechnologyRepository):
    data = request.get_json()
    current_technology = technology_repository.get_by_id(technology_id)
    if not current_technology:
        return jsonify({"error": "Technology not found"}), 404

    updated_technology = TechnologyModel(
        _id=current_technology.id,
        technology=data.get("technology", current_technology.technology),
        stages=data.get("stages", current_technology.stages),
        created_at=current_technology.created_at,
        updated_at=datetime.utcnow()
    )

    updated = technology_repository.update(technology_id, updated_technology)
    if updated:
        return jsonify({"message": "Technology updated successfully"}), 200
    return jsonify({"error": "Update failed"}), 400


@technology_routes.route('/technologies/<string:technology_id>', methods=['DELETE'])
@inject
def delete_technology(technology_id, technology_repository: TechnologyRepository):
    deleted = technology_repository.delete(technology_id)
    if deleted:
        return jsonify({"message": "Technology deleted successfully"}), 200
    return jsonify({"error": "Technology not found"}), 404
