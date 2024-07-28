from flask import Flask
from flask_injector import FlaskInjector
from injector import singleton, Binder
from services.ai_generation_service import AIGenerationService
from flask_injector import FlaskInjector

def create_app() -> Flask:
    app = Flask(__name__)
    
    with app.app_context():
        from routes import bp  # Import the blueprint
        app.register_blueprint(bp)  # Register the blueprint
    
    return app


def configure(binder: Binder) -> None:
    binder.bind(AIGenerationService, to=AIGenerationService, scope=singleton)

def main():
    app = create_app()
    FlaskInjector(app=app, modules=[configure])
    app.run(host='0.0.0.0', port=3333) 

if __name__ == "__main__":
    main()