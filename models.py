from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pass_helper
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    def __repr__(self):
        return '<User %r>' % self.email
    def hash_password(self,password):
        self.password = pass_helper.encrypt(password)
    def verify_password(self,password):
        return pass_helper.verify(password,self.password)