from flask import Flask, jsonify
from flask_cors import CORS
import os
from .database import close_db


def create_app() -> Flask:
    """Flask application factory."""
    app = Flask(__name__, static_folder=None)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        API_PREFIX=os.environ.get("API_PREFIX", "/api"),
        DB_NAME=os.environ.get("DB_NAME"),
        DB_USERNAME=os.environ.get("DB_USERNAME"),
        DB_PASSWORD=os.environ.get("DB_PASSWORD"),
        DB_HOST=os.environ.get("DB_HOST", "localhost"),
        DB_PORT=os.environ.get("DB_PORT", "5432"),
    )

    CORS(app)
    app.teardown_appcontext(close_db)

    @app.route(app.config["API_PREFIX"] + "/health", methods=["GET"])
    def health() -> dict:
        """Health check endpoint."""
        return jsonify({"status": "ok"})

    # Blueprints
    from .students.routes import bp as students_bp
    from .programs.routes import bp as programs_bp
    from .colleges.routes import bp as colleges_bp
    from .auth.routes import bp as auth_bp

    base = app.config["API_PREFIX"]
    app.register_blueprint(auth_bp, url_prefix=f"{base}/auth")
    app.register_blueprint(colleges_bp, url_prefix=f"{base}/colleges")
    app.register_blueprint(programs_bp, url_prefix=f"{base}/programs")
    app.register_blueprint(students_bp, url_prefix=f"{base}/students")

    return app
