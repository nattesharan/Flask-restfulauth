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
class PrivateResource(Resource):
    def get(self):
        return {
            'message': 'Auth required'
        }