from flask_httpauth import HTTPBasicAuth
from models import User
auth = HTTPBasicAuth()
@auth.verify_password
def verify_password(username,password):
    if not (username and password):
        return False
    user = User.query.filter_by(email=username).first()
    print user
    return user.verify_password(password)
