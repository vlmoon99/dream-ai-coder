import logging
from flask import Blueprint, jsonify, render_template, request
from flask_injector import inject
from ..repositories.project_repository import ProjectRepository
from ..models.project_model import ProjectModel
from datetime import datetime

project_routes = Blueprint('project', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@project_routes.route('/')
def index():
    return render_template('index.html')


@project_routes.route('/create-project', methods=['POST'])
@inject
def create_project(project_repository: ProjectRepository):
    data = request.get_json()
    project = ProjectModel(name=data['name'], technology=data['technology'],current_stage=1)
    created_project = project_repository.create(project)
    return jsonify(created_project.to_dict()), 201



@project_routes.route('/projects/<string:project_id>', methods=['GET'])
@inject
def get_project(project_id, project_repository: ProjectRepository):
    project = project_repository.get_by_id(project_id)
    if project:
        return jsonify(project.to_dict()), 200
    return jsonify({"error": "Project not found"}), 404


@project_routes.route('/projects/<string:project_id>', methods=['PUT'])
@inject
def update_project(project_id, project_repository: ProjectRepository):
    data = request.get_json()
    current_project = project_repository.get_by_id(project_id)
    if not current_project:
        return jsonify({"error": "Project not found"}), 404

    updated_project = ProjectModel(
        _id=current_project.id,
        name=data.get("name", current_project.name),
        created_at=current_project.created_at, 
        updated_at=datetime.utcnow() 
    )

    updated = project_repository.update(project_id, updated_project)
    if updated:
        return jsonify({"message": "Project updated successfully"}), 200
    return jsonify({"error": "Update failed"}), 400


@project_routes.route('/projects/<string:project_id>', methods=['DELETE'])
@inject
def delete_project(project_id, project_repository: ProjectRepository):
    deleted = project_repository.delete(project_id)
    if deleted:
        return jsonify({"message": "Project deleted successfully"}), 200
    return jsonify({"error": "Project not found"}), 404
