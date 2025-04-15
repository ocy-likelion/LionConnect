from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import timedelta
import os
from dotenv import load_dotenv
from extensions import db, bcrypt, jwt, migrate
from flask_restx import Api
from config import Config

# .env 파일 로드
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# CORS 설정
CORS(app, resources={r"/*": {
    "origins": [
        "http://localhost:3000",
        "https://lion-connect.vercel.app"
    ],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization", "Accept"],
    "expose_headers": ["Authorization"],
    "supports_credentials": True,
    "max_age": 3600
}})

# 확장 초기화
db.init_app(app)
bcrypt.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)

# Swagger UI 설정
api = Api(
    app,
    version='1.0',
    title='Lion Connect API',
    description='Lion Connect 백엔드 API 문서',
    doc='/docs'
)

# 업로드 폴더가 없으면 생성
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# 파일 확장자 검사 함수
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# 기본 라우트
@app.route('/')
def welcome():
    return jsonify({
        'message': 'Welcome to Lion Connect API',
        'documentation': '/docs'
    })

# 라우트와 API 모델 등록
from routes.auth import auth_ns
from routes.user import user_ns
from routes.company import company_ns

# 네임스페이스 등록
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(user_ns, path='/user')
api.add_namespace(company_ns, path='/company')

# 블루프린트 등록
from routes.auth import auth_bp
from routes.user import user_bp
from routes.company import company_bp

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(company_bp)

# JWT 에러 핸들러
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'message': 'The token has expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'status': 401,
        'sub_status': 43,
        'message': 'Invalid token'
    }), 401

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True) 