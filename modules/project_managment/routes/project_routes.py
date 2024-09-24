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
    """
    Create a new project.
    ---
    tags:
      - Project
    parameters:
      - name: project
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            technology:
              type: string
    responses:
      201:
        description: Project created successfully
        schema:
          type: object
          properties:
            id:
              type: string
            name:
              type: string
            technology:
              type: string
            current_stage:
              type: integer
      400:
        description: Invalid input
    """
    data = request.get_json()
    project = ProjectModel(
        name=data['name'], technology=data['technology'], current_stage=1, generated_files=[])
    created_project = project_repository.create(project)
    return jsonify(created_project.to_dict()), 201


@project_routes.route('/projects/<string:project_id>', methods=['GET'])
@inject
def get_project(project_id, project_repository: ProjectRepository):
    """
    Get a project by ID.
    ---
    tags:
      - Project
    parameters:
      - name: project_id
        in: path
        required: true
        type: string
    responses:
      200:
        description: Project retrieved successfully
        schema:
          type: object
          properties:
            id:
              type: string
            name:
              type: string
            technology:
              type: string
            current_stage:
              type: integer
      404:
        description: Project not found
    """
    project = project_repository.get_by_id(project_id)
    if project:
        return jsonify(project.to_dict()), 200
    return jsonify({"error": "Project not found"}), 404


@project_routes.route('/projects/<string:project_id>', methods=['PUT'])
@inject
def update_project(project_id, project_repository: ProjectRepository):
    """
    Update an existing project by ID.
    ---
    tags:
      - Project
    parameters:
      - name: project_id
        in: path
        required: true
        type: string
      - name: project
        in: body
        required: false
        schema:
          type: object
          properties:
            name:
              type: string
    responses:
      200:
        description: Project updated successfully
      404:
        description: Project not found
      400:
        description: Update failed
    """
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
    """
    Delete a project by ID.
    ---
    tags:
      - Project
    parameters:
      - name: project_id
        in: path
        required: true
        type: string
    responses:
      200:
        description: Project deleted successfully
      404:
        description: Project not found
    """
    deleted = project_repository.delete(project_id)
    if deleted:
        return jsonify({"message": "Project deleted successfully"}), 200
    return jsonify({"error": "Project not found"}), 404
