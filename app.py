from flask import Flask
from flask_injector import FlaskInjector
from injector import singleton, Binder
from services.ai_generation_service import AIGenerationService
from flask_injector import FlaskInjector
from services.video_streaming_service import VideoStreamingService  # Import the VideoStreamingService

def create_app() -> Flask:
    app = Flask(__name__, static_folder='static', template_folder='templates')

    with app.app_context():
        from routes import bp  
        app.register_blueprint(bp)
    
    return app


def configure(binder: Binder) -> None:
    binder.bind(AIGenerationService, to=AIGenerationService, scope=singleton)
    binder.bind(VideoStreamingService, to=VideoStreamingService, scope=singleton)  # Corrected




def main():
    app = create_app()
    FlaskInjector(app=app, modules=[configure])
    app.run(host='0.0.0.0', port=3333)
    return app

if __name__ == "__main__":
  flask_app =  main()
  