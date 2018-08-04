from flask import request,jsonify
from functools import wraps
from models import User
from config import SECRET_KEY
import jwt
def token_required(f):
    @wraps(f)
    def decorated_func(*args,**kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({
                'message': 'Token required'
            })
        try:
            data = jwt.decode(token,SECRET_KEY)
            current_user = User.query.filter_by(public_id=data['public_id']).first()
            return f(current_user,*args,**kwargs)
        except Exception as E:
            print E
            return jsonify({
                'message': 'Token is invalid'
            })
    return decorated_func