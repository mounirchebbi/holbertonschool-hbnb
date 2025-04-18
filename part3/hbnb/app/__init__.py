# app/__init__.py

from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as login_ns
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.database import db  # Import db from the new module

# Instantiate Flask extensions
bcrypt = Bcrypt()
jwt = JWTManager()

# Create and configure the Flask app
def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Set up the REST API with Flask-RESTX
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')
    
    # Register API namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1')
    api.add_namespace(login_ns, path='/api/v1')
    
    return app
