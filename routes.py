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
def index(ai_generation_service: AIGenerationService):
    return jsonify({
        "message": "Welcome to the AI Coder Machine Console App!",
        "status": "success"
    })

# Add more routes as needed
@bp.route('/generate', methods=['POST'])
@inject
def generate_code(ai_generation_service: AIGenerationService):
    # Logic to generate code using ai_generation_service
    result = ai_generation_service.generate_code()
    return jsonify(result)
