from flask import Blueprint
from flask_restful import Api
import resources

api_bp = Blueprint('api',__name__)
api = Api(api_bp)

api.add_resource(resources.UserRegistration,'/registration')
api.add_resource(resources.UserLogin,'/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.PrivateResource,'/test/auth')