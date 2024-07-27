from flask_restful import Api
from flask import Blueprint

# Initialize Blueprint for API routes
api_bp = Blueprint('api', __name__)
api = Api(api_bp)
