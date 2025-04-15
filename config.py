import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 기본 설정
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    
    # 데이터베이스 설정
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:uo7c6gbQ6VmhYkqRfs9YtNnb0Ud9O3ky@localhost:5432/lion_connect')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT 설정
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_ERROR_MESSAGE_KEY = 'error'
    JWT_BLACKLIST_ENABLED = False
    
    # 파일 업로드 설정
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} 