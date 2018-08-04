from flask import Flask
from flask_jwt_extended import JWTManager
from models import RevokedTokenModel
def create_app(config):
    app = Flask(__name__)
    app.secret_key = 'TOKENAUTHAPP'
    app.config.from_object(config)
    jwt = JWTManager(app)
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return RevokedTokenModel.is_jti_blacklisted(jti)
    from app import api_bp
    app.register_blueprint(api_bp)
    from models import db
    db.init_app(app)
    return app
if __name__ == '__main__':
    app = create_app('config')
    app.run(port=3000,debug=True)