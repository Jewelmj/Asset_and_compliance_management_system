from flask import Flask
from api.routes.assets import assets_bp
from api.routes.places import places_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(assets_bp, url_prefix="/api/assets")
    app.register_blueprint(places_bp, url_prefix="/api/places")

    @app.get("/")
    def health():
        return {"status": "ok", "message": "API is running"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)