from flask_restful import Resource,reqparse
from flask import request
from models import User,db
parser = reqparse.RequestParser()
parser.add_argument('email',help='This fielld cannot be blank',required=True)
parser.add_argument('password',help='This fielld cannot be blank',required=True)
class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        email = data['email']
        if User.find_user(email) is not None:
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
        data = parser.parse_args()
        user = User.find_user(data['email'])
        if not user:
            return {
                'message': 'User not found'
            },404
        elif user.verify_password(data['password']):
            return {
                'message': 'Logged in as {}'.format(user.email.split('@')[0])
            }
        else:
            return {
                'message': 'Invalid credentials'
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
        return User.return_all()

    def delete(self):
        return User.delete_all()

class PrivateResource(Resource):
    def get(self):
        return {
            'message': 'Auth required'
        }