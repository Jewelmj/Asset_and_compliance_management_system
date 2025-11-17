from flask import Flask
from flask_jwt_extended import JWTManager
from api.config import get_config
from api.routes.assets import assets_bp
from api.routes.places import places_bp
from api.routes.projects import projects_bp
from api.routes.auth import auth_bp
from api.routes.subcontractors import subcontractors_bp


def create_app():
    app = Flask(__name__)
    
    # Load configuration
    config = get_config()
    app.config.from_object(config)
    
    # Initialize JWT
    jwt = JWTManager(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(assets_bp, url_prefix="/api/assets")
    app.register_blueprint(projects_bp, url_prefix="/api/projects")
    app.register_blueprint(places_bp, url_prefix="/api/places")
    app.register_blueprint(subcontractors_bp, url_prefix="/api/subcontractors")

    @app.get("/")
    def health():
        return {"status": "ok", "message": "API is running"}

    return app


app = create_app()

if __name__ == "__main__":
    import os
    debug = os.getenv("FLASK_ENV", "production") == "development"
    app.run(host="0.0.0.0", port=5000, debug=debug)