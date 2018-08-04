from flask_restful import Resource,reqparse
from sqlalchemy.orm.exc import NoResultFound
from flask import request
from models import User,db
from utils import token_required
import uuid
import jwt
import datetime
from config import SECRET_KEY
parser = reqparse.RequestParser()
parser.add_argument('email',help='This fielld cannot be blank',required=True)
parser.add_argument('password',help='This fielld cannot be blank',required=True)
class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        is_admin = data['is_admin']
        if User.find_user(email) is not None:
            return {
                'message': "User already exists with that name"
            }
        user = User(email=email,public_id=str(uuid.uuid4()),is_admin=is_admin)
        user.hash_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return {
            'message': 'Successfully added user'
        }
class Login(Resource):
    def post(self):
        data = parser.parse_args()
        user = User.find_user(data['email'])
        if not user:
            return {
                'message': 'User does not exist'
            }
        elif user.verify_password(data['password']):
            token = jwt.encode({'public_id': user.public_id,'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},SECRET_KEY)
            return {
                'message': 'logged in as {}'.format(user.email.split('@')[0]),
                'token': token.decode('UTF-8')
            }
        else:
            return {
                'message': 'Invalid credentials'
            }
class FetchUsers(Resource):
    method_decorators = [token_required]
    def get(self,current_user):
        if not current_user.is_admin:
            return {
                'message': 'You are not allowed for this action'
            }
        return User.return_all()

class FetchUser(Resource):
    method_decorators = [token_required]
    def get(self,current_user,user_id):
        if not current_user.is_admin:
            return {
                'message': 'You are not allowed for this action'
            }
        try:
            user = User.query.filter_by(id=user_id).first()
            if user:
                return {
                    'email': user.email,
                    'password': user.password,
                    'is_admin': user.is_admin,
                    'id': user.id,
                    'public_id': user.public_id
                }
            return {
                'message': 'No user available with that id'
            }
        except:
            return {
                'message': 'Some error occured'
            }
    def put(self,current_user,user_id):
        if not current_user.is_admin:
            return {
                'message': 'You are not allowed for this action'
            }
        try:
            user = User.query.filter_by(id=user_id).first()
            if user:
                user.is_admin = True
                db.session.commit()
                return {
                    'message': 'Successfully promoted'
                }
            return {
                'message': 'No user available with that id'
            }
        except:
            return {
                'message': 'Some error occured'
            }
    def delete(self,current_user,user_id):
        if not current_user.is_admin:
            return {
                'message': 'You are not allowed for this action'
            }
        try:
            user = User.query.filter_by(id=user_id).first()
            if user:
                db.session.delete(user)
                db.session.commit()
                return {
                    'message': 'Successfully Deleted User'
                }
            return {
                'message': 'No user available with that id'
            }
        except Exception as E:
            return {
                'message': 'Some error occured'
            }
class PrivateResource(Resource):
    method_decorators = [token_required]
    def get(self,current_user):
        return {
            'message': 'Auth required'
        }