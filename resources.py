from flask_restful import Resource
from flask import request
from models import User,db
class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        if User.query.filter_by(email=email).first() is not None:
            return {
                'message': "User already exists with that name"
            }
        user = User(email=email)
        user.hash_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return {
            'message': 'Successfully added user'
        }
class UserLogin(Resource):
    def post(self):
        return {
            'message': "hello"
        }
class UserLogoutAccess(Resource):
    def post(self):
        return {'message': 'User logout'}
      
      
class UserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'User logout'}
      
      
class TokenRefresh(Resource):
    def post(self):
        return {'message': 'Token refresh'}

class AllUsers(Resource):
    def get(self):
        return {'message': 'List of users'}

    def delete(self):
        return {'message': 'Delete all users'}

class PrivateResource(Resource):
    def get(self):
        return {
            'message': 'Auth required'
        }