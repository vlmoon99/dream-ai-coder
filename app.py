from flask import Flask
from flask_injector import FlaskInjector
from injector import singleton, Binder
from services.ai_generation_service import AIGenerationService
from flask_injector import FlaskInjector
from services.video_streaming_service import VideoStreamingService  # Import the VideoStreamingService

#Import all dependencies from modules
from modules.project_managment.repositories.project_repository import ProjectRepository

from modules.project_managment.routes.project import project_routes


def create_app() -> Flask:
    app = Flask(__name__, static_folder='static', template_folder='templates')

    with app.app_context():
        app.register_blueprint(project_routes)
    
    return app


def configure(binder: Binder) -> None:
    binder.bind(AIGenerationService, to=AIGenerationService, scope=singleton)
    binder.bind(VideoStreamingService, to=VideoStreamingService, scope=singleton)  
    binder.bind(ProjectRepository, to=ProjectRepository,
                scope=singleton) 


def main():
    app = create_app()
    FlaskInjector(app=app, modules=[configure])
    app.run(host='0.0.0.0', port=3333, debug=True)
    return app

if __name__ == "__main__":
  flask_app =  main()