from flask_restful import Resource,reqparse
from flask import request
from models import User,db,RevokedTokenModel
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,
                                jwt_refresh_token_required,get_jwt_identity,get_raw_jwt)
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
        access_token = create_access_token(identity=user.email)
        refresh_token = create_refresh_token(identity=user.email)
        return {
            'message': 'Successfully added user',
            'access_token': access_token,
            'refresh_token': refresh_token
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
            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)
            return {
                'message': 'Logged in as {}'.format(user.email.split('@')[0]),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {
                'message': 'Invalid credentials'
            }
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        revoked_token = RevokedTokenModel(jti=jti)
        db.session.add(revoked_token)
        db.session.commit()
        return {'message': 'Access token has been revoked'}
      
      
class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        revoked_token = RevokedTokenModel(jti=jti)
        db.session.add(revoked_token)
        db.session.commit()
        return {'message': 'Refresh token has been revoked'}
      
      
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}

class AllUsers(Resource):
    def get(self):
        return User.return_all()

    def delete(self):
        return User.delete_all()

class PrivateResource(Resource):
    @jwt_required
    def get(self):
        return {
            'message': 'Auth required'
        }