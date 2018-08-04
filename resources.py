from flask_restful import Resource
from flask import request
from models import User,db
from utils import auth
class Users(Resource):
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

class PrivateResource(Resource):
    @auth.login_required
    def get(self):
        return {
            'message': 'Auth required'
        }