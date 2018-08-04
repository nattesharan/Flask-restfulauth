from flask import Blueprint
from flask_restful import Api
from resources import PrivateResource,Users

api_bp = Blueprint('api',__name__)
api = Api(api_bp)

api.add_resource(Users,'/create/user')
api.add_resource(PrivateResource,'/test/auth')