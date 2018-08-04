from flask_sqlalchemy import SQLAlchemy
# from passlib.apps import custom_app_context as pass_helper
from passlib.hash import pbkdf2_sha256 as sha256
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    def __repr__(self):
        return '<User %r>' % self.email
    def hash_password(self,password):
        # self.password = pass_helper.encrypt(password)
        self.password = sha256.hash(password)
    def verify_password(self,password):
        # return pass_helper.verify(password,self.password)
        return sha256.verify(password,self.password)
    @classmethod
    def find_user(cls,email):
        return cls.query.filter_by(email=email).first()
    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'email': x.email,
                'password': x.password
            }
        return {
            'users': list(map(lambda x:to_json(x),cls.query.all()))
        }
    @classmethod
    def delete_all(cls):
        num_rows = db.session.query(cls).delete()
        db.session.commit()
        return {'message': '{} row(s) deleted'.format(num_rows)}
    
class RevokedTokenModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(512))

    @classmethod
    def is_jti_blacklisted(cls,jti):
        token = cls.query.filter_by(jti=jti).first()
        return bool(token)