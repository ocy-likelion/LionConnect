from flask import Flask, request, jsonify, current_app
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import timedelta
import os
from dotenv import load_dotenv
from extensions import db, bcrypt, jwt, migrate
from flask_restx import Api, Resource, fields

# .env 파일 로드
load_dotenv()

app = Flask(__name__)
CORS(app)

# Swagger UI 설정
api = Api(
    app,
    version='1.0',
    title='Lion Connect API',
    description='Lion Connect 백엔드 API 문서',
    doc='/docs'
)

# API 모델 정의
user_model = api.model('User', {
    'email': fields.String(required=True, description='사용자 이메일'),
    'password': fields.String(required=True, description='비밀번호'),
    'name': fields.String(required=True, description='이름'),
    'user_type': fields.String(required=True, description='사용자 타입 (student/company)'),
    'course': fields.String(description='수강 코스 (student만 해당)'),
    'skills': fields.List(fields.String, description='기술 스택 (student만 해당)'),
    'portfolio': fields.String(description='포트폴리오 URL (student만 해당)'),
    'company_name': fields.String(description='회사명 (company만 해당)'),
    'industry': fields.String(description='산업 분야 (company만 해당)'),
    'company_size': fields.String(description='회사 규모 (company만 해당)'),
    'company_location': fields.String(description='회사 위치 (company만 해당)')
})

login_model = api.model('Login', {
    'email': fields.String(required=True, description='사용자 이메일'),
    'password': fields.String(required=True, description='비밀번호')
})

resume_model = api.model('Resume', {
    'name': fields.String(required=True, description='이름'),
    'email': fields.String(required=True, description='이메일'),
    'phone': fields.String(description='전화번호'),
    'introduction': fields.String(description='자기소개'),
    'workExperience': fields.List(fields.Nested(api.model('WorkExperience', {
        'company': fields.String(required=True),
        'position': fields.String(required=True),
        'startDate': fields.String(required=True),
        'endDate': fields.String(required=True),
        'description': fields.String()
    }))),
    'projects': fields.List(fields.Nested(api.model('Project', {
        'title': fields.String(required=True),
        'description': fields.String(required=True),
        'startDate': fields.String(required=True),
        'endDate': fields.String(required=True),
        'techStack': fields.List(fields.String())
    }))),
    'skills': fields.List(fields.String()),
    'education': fields.List(fields.Nested(api.model('Education', {
        'school': fields.String(required=True),
        'major': fields.String(required=True),
        'degree': fields.String(required=True),
        'startDate': fields.String(required=True),
        'endDate': fields.String(required=True)
    })))
})

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
api.add_namespace(auth_api, path='/api/auth')
api.add_namespace(user_api, path='/api/user')

# 파일 확장자 검사 함수
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@api.route('/')
class Welcome(Resource):
    def get(self):
        """API 기본 정보를 반환합니다."""
        return {
            'message': 'Lion Connect API에 오신 것을 환영합니다!',
            'version': '1.0.0',
            'documentation': '/docs'
        }

if __name__ == '__main__':
    app.run(debug=True) 