from flask import Flask
from flask_cors import CORS
import os

def create_app():
    """Application Factory"""
    app = Flask(__name__, static_folder=None)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        API_PREFIX=os.environ.get("API_PREFIX", "/api"),
    )

    CORS(app)
    
    from .api.students import bp as students_bp
    app.register_blueprint(students_bp, url_prefix=app.config["API_PREFIX"] + "/students")

    return app