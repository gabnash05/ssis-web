from datetime import timedelta
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from .db.database import close_db

jwt = JWTManager()

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
        JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY", "super-secret"),
        JWT_TOKEN_LOCATION=["cookies"],
        JWT_COOKIE_SECURE=False,  # True in production (HTTPS only)
        JWT_COOKIE_HTTPONLY=True,
        JWT_COOKIE_SAMESITE="Lax",
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_HOURS", 1))),
        JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 10))),
    )

    # CORS configuration
    # origins = os.environ.get("CORS_ORIGINS", "http://localhost:5173")
    # origins = origins.split(",")

    origins = ["http://localhost:5173"]
    CORS(app, 
         supports_credentials=True, 
         origins=origins,
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], 
         allow_headers=["Content-Type", "Authorization", "X-CSRF-Token"]
    )
    
    
    app.teardown_appcontext(close_db)
    app.url_map.strict_slashes = False
    
    jwt.init_app(app)

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
