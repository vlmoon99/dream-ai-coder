from flask import Flask
from flask_injector import FlaskInjector
from injector import singleton, Binder
from flask_injector import FlaskInjector
from flasgger import Swagger
import logging

from modules.project_managment.repositories.project_repository import ProjectRepository
from modules.project_managment.routes.project_routes import project_routes

from modules.code_generation.repositories.template_repository import TemplateRepository
from modules.code_generation.routes.template_routes import template_routes

from modules.code_generation.repositories.technology_repository import TechnologyRepository
from modules.code_generation.routes.technology_routes import technology_routes

from modules.code_generation.services.ollama_service import OlamaService
from modules.code_generation.services.file_service import FileService
from modules.code_generation.services.command_line_execution_service import CommandLineExecutionService
from modules.code_generation.routes.generation_routes import generation_routes


def create_app() -> Flask:
    app = Flask(__name__, static_folder='static', template_folder='templates')


    logging.getLogger('pymongo').setLevel(logging.WARNING)

    swagger = Swagger(app)

    with app.app_context():
        app.register_blueprint(project_routes)
        app.register_blueprint(template_routes)
        app.register_blueprint(technology_routes)
        app.register_blueprint(generation_routes)

    return app


def configure(binder: Binder) -> None:
    binder.bind(ProjectRepository, to=ProjectRepository,
                scope=singleton) 
    binder.bind(TemplateRepository, to=TemplateRepository,
                scope=singleton)
    binder.bind(TechnologyRepository, to=TechnologyRepository,
                scope=singleton)
    binder.bind(OlamaService, to=OlamaService,
                scope=singleton)
    binder.bind(FileService, to=FileService,
                scope=singleton)
    binder.bind(CommandLineExecutionService, to=CommandLineExecutionService,
                scope=singleton)




def main():
    app = create_app()
    FlaskInjector(app=app, modules=[configure])
    app.run(host='0.0.0.0', port=3333, debug=True)
    return app

if __name__ == "__main__":
  flask_app =  main()