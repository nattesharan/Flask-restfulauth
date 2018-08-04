from flask_sqlalchemy import SQLAlchemy
# from passlib.apps import custom_app_context as pass_helper
# from passlib.hash import pbkdf2_sha256 as sha256
from werkzeug.security import generate_password_hash,check_password_hash
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean)
    def __repr__(self):
        return '<User %r>' % self.email
    def hash_password(self,password):
        # self.password = pass_helper.encrypt(password)
        # self.password = sha256.hash(password)
        self.password = generate_password_hash(password,method='sha256')
    def verify_password(self,password):
        # return pass_helper.verify(password,self.password)
        # return sha256.verify(password,self.password)
        return check_password_hash(self.password,password)
    @classmethod
    def find_user(cls,email):
        return cls.query.filter_by(email=email).first()
    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'email': x.email,
                'password': x.password,
                'is_admin': x.is_admin,
                'public_id': x.public_id,
                'id': x.id
            }
        return {
            'users': list(map(lambda x:to_json(x),cls.query.all()))
        }