from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_migrate import Migrate
from flask import jsonify

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

@jwt.user_identity_loader
def user_identity_lookup(user):
    if isinstance(user, int):
        return str(user)
    return str(user.id)

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    from models import User
    identity = jwt_data["sub"]
    return User.query.get(identity)

@jwt.unauthorized_loader
def unauthorized_callback(callback):
    return jsonify({
        'error': 'Unauthorized',
        'message': 'Missing or invalid token'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(callback):
    return jsonify({
        'error': 'Invalid token',
        'message': 'Signature verification failed'
    }), 401 