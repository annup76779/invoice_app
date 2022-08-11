from flask import Flask, current_app,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
crypt = Bcrypt()

def create_app(config_cls=None):
    app = Flask(__name__)

    # import the custom configurations for the app
    import configmodule
    if config_cls is None:
        if app.config["ENV"] == "production":
            app.config.from_object(configmodule.Production)
        else:
            app.config.from_object(configmodule.Development)
    else:
        app.config.from_object(configmodule.Test)

    initialize_extensions(app) # getting extensions ready for the work
    register_blueprint(app) # registering the blueprint for the app
    register_error_handler(app) # registering the error handler for the app
    return app

def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db = db)
    # with app.app_context():
        # upgrade()

    from app.model import Admin
    jwt.init_app(app)

    # callback function to load users.user_id when serializing the jwt identity
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user

    # callback function to load the user object when any protected route in accessed
    # this function takes user_id from the jwt and loads the user accordingly
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        if isinstance(identity,str) and identity.isnumeric():
            return Admin.query.get(int(identity))
        elif isinstance(identity, int):
            return Admin.query.get(identity)

    crypt.init_app(app) # initializing the crypto


def register_blueprint(app):
    #-----------------------------------------------------------------------------
    # registering the blueprint responsible for login/register and authentication
    #-----------------------------------------------------------------------------
    from app.admin import admin_bp as admin
    app.register_blueprint(admin)
    os.makedirs(name = os.path.join(app.root_path, admin.static_folder), exist_ok = True)

    from app.general import general_bp
    app.register_blueprint(general_bp)
    # os.makedirs(name = os.path.join(app.root_path, general_bp.static_folder, "feedback"), exist_ok = True)

def register_error_handler(app):
    @app.errorhandler(500)
    def error_505_handler(error):
        return jsonify(error = "Internal Server Error")
