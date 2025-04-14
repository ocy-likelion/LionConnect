from flask import Flask, request, jsonify, current_app
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import timedelta
import os
from dotenv import load_dotenv
from extensions import db, bcrypt, jwt, migrate

# .env 파일 로드
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

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
    from routes.auth import auth_bp
    from routes.user import user_bp

    # 블루프린트 등록
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')

    # 파일 확장자 검사 함수
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    @app.route('/')
    def welcome():
        return jsonify({
            'message': 'Lion Connect API에 오신 것을 환영합니다!',
            'version': '1.0.0',
            'endpoints': {
                'auth': {
                    'signup': '/api/auth/signup',
                    'login': '/api/auth/login'
                },
                'users': {
                    'profile': '/api/users/profile',
                    'resume': '/api/users/resume'
                },
                'posts': {
                    'list': '/api/posts',
                    'create': '/api/posts'
                },
                'matches': {
                    'suggestions': '/api/matches/suggestions'
                }
            }
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 