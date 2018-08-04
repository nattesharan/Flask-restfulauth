from flask import Flask
from flask_jwt_extended import JWTManager
def create_app(config):
    app = Flask(__name__)
    app.secret_key = 'TOKENAUTHAPP'
    app.config.from_object(config)
    jwt = JWTManager(app)
    from app import api_bp
    app.register_blueprint(api_bp)
    from models import db
    db.init_app(app)
    return app
if __name__ == '__main__':
    app = create_app('config')
    app.run(port=3000,debug=True)