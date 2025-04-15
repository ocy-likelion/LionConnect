from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_cors import CORS
from datetime import timedelta
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def init_extensions(app):
    # CORS 설정
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000", "https://lion-connect-frontend.onrender.com"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Origin"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "max_age": 600
        }
    })
    
    # 데이터베이스 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:uo7c6gbQ6VmhYkqRfs9YtNnb0Ud9O3ky@localhost:5432/lion_connect')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 데이터베이스 연결 타임아웃 설정
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_timeout': 30,  # 연결 풀 타임아웃 (초)
        'pool_recycle': 1800,  # 연결 재사용 시간 (30분)
        'pool_pre_ping': True,  # 연결 상태 확인
        'connect_args': {
            'connect_timeout': 10,  # 연결 시도 타임아웃 (초)
            'application_name': 'lion_connect'  # 애플리케이션 식별자
        }
    }
    
    # JWT 설정
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
    app.config['JWT_ERROR_MESSAGE_KEY'] = 'message'
    
    # 확장 초기화
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # JWT 에러 핸들러
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return {
            'message': '인증이 필요합니다.',
            'error': 'unauthorized'
        }, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        return {
            'message': '유효하지 않은 토큰입니다.',
            'error': 'invalid_token'
        }, 401
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {
            'message': '만료된 토큰입니다.',
            'error': 'token_expired'
        }, 401 