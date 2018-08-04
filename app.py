from flask import Blueprint
from flask_restful import Api
import resources

api_bp = Blueprint('api',__name__)
api = Api(api_bp)

api.add_resource(resources.UserRegistration,'/registration')
api.add_resource(resources.Login,'/login')
api.add_resource(resources.FetchUsers,'/users')
api.add_resource(resources.FetchUser,'/user/<int:user_id>')
api.add_resource(resources.PrivateResource,'/test/auth')