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
CORS(app)

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
    doc='/docs',
    prefix='/api'
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

api.add_namespace(auth_ns)
api.add_namespace(user_ns)

if __name__ == '__main__':
    app.run(debug=True) 