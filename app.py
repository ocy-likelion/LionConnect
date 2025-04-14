from flask import Flask, request, jsonify, current_app
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import timedelta
import os
from dotenv import load_dotenv
from extensions import db, bcrypt, jwt, migrate
from flask_restx import Api, Resource, fields
from config import Config
from models import User
from models.api_models import create_api_models

# .env 파일 로드
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Swagger UI 설정
api = Api(
    app,
    version='1.0',
    title='Lion Connect API',
    description='Lion Connect 백엔드 API 문서',
    doc='/docs',
    prefix='/api'
)

# API 모델 생성
api_models = create_api_models(api)
login_model = api_models['login_model']
signup_model = api_models['signup_model']
resume_model = api_models['resume_model']

# 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:1234@localhost:5432/lion_connect')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT 설정
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['JWT_ERROR_MESSAGE_KEY'] = 'error'
app.config['JWT_BLACKLIST_ENABLED'] = False

# 파일 업로드 설정
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# 업로드 폴더가 없으면 생성
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# 확장 초기화
db.init_app(app)
bcrypt.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)

# 모델 import
from models import User, WorkExperience, Project, Skill, Education, Award, Certificate

# 라우트 import
from routes.auth import auth_bp, api as auth_api
from routes.user import user_bp, api as user_api

# API 네임스페이스 등록
auth_ns = api.namespace('auth', description='인증 관련 API')
user_ns = api.namespace('user', description='사용자 관련 API')

# 파일 확장자 검사 함수
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@api.route('/')
class Welcome(Resource):
    def get(self):
        """API 기본 정보를 반환합니다."""
        return {
            'message': 'Welcome to Lion Connect API',
            'documentation': '/docs'
        }

# 블루프린트를 API 네임스페이스에 등록
from routes.auth import Login, Signup
from routes.user import Resume

auth_ns.add_resource(Login, '/login')
auth_ns.add_resource(Signup, '/signup')
user_ns.add_resource(Resume, '/resume')

if __name__ == '__main__':
    app.run(debug=True) 