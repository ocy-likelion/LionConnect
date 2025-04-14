from flask import Blueprint, request, jsonify
from models import User, Skill
from extensions import db, bcrypt, jwt, create_access_token
from flask_restx import Resource, Namespace
import re
from app import api, user_model, login_model, signup_model

auth_bp = Blueprint('auth', __name__)
api = Namespace('auth', description='인증 관련 API')

def validate_password(password):
    """비밀번호 유효성 검사"""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Za-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

@api.route('/signup')
class Signup(Resource):
    @api.doc('새로운 사용자 등록',
             description='''
             새로운 사용자를 등록합니다.
             
             사용자 유형:
             - student: 학생 (기술 스택 필수)
             - company: 기업 (회사명, 회사 소개 필수)
             
             요청 데이터:
             - email: 사용자 이메일 (필수)
             - password: 비밀번호 (필수, 8자 이상, 영문/숫자/특수문자 포함)
             - name: 이름 (필수)
             - user_type: 사용자 타입 (필수, 'student' 또는 'company')
             
             student 타입일 경우 추가 필드:
             - course: 수강 코스
             - skills: 기술 스택 목록
             - portfolio: 포트폴리오 URL
             
             company 타입일 경우 추가 필드:
             - company_name: 회사명
             - industry: 산업 분야
             - company_size: 회사 규모
             - company_location: 회사 위치
             
             응답:
             201: 회원가입 성공
             400: 필수 필드 누락 또는 유효하지 않은 데이터
             409: 이메일 중복
             500: 서버 오류
             ''',
             responses={
                 201: '회원가입 성공',
                 400: '필수 필드 누락 또는 유효하지 않은 데이터',
                 409: '이메일 중복',
                 500: '서버 오류'
             })
    @api.expect(signup_model)
    def post(self):
        """새로운 사용자를 등록합니다."""
        try:
            data = request.get_json()
            
            # 필수 필드 검사
            required_fields = ['email', 'password', 'name', 'user_type']
            if not all(field in data for field in required_fields):
                return {'error': 'Missing required fields'}, 400
            
            # 이메일 중복 검사
            if User.query.filter_by(email=data['email']).first():
                return {'error': 'Email already exists'}, 409
            
            # 사용자 유형별 추가 필드 검사
            if data['user_type'] == 'student':
                if 'skills' not in data or not data['skills']:
                    return {'error': 'Skills are required for student'}, 400
            elif data['user_type'] == 'company':
                if 'company_name' not in data or 'company_description' not in data:
                    return {'error': 'Company name and description are required for company'}, 400
            else:
                return {'error': 'Invalid user type'}, 400
            
            # 새 사용자 생성
            user = User(
                email=data['email'],
                name=data['name'],
                user_type=data['user_type']
            )
            user.set_password(data['password'])
            
            # 사용자 유형별 추가 정보 저장
            if data['user_type'] == 'student':
                user.skills = data['skills']
            else:
                user.company_name = data['company_name']
                user.company_description = data['company_description']
            
            db.session.add(user)
            db.session.commit()
            
            return {'message': 'User created successfully'}, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

@api.route('/login')
class Login(Resource):
    @api.doc('사용자 로그인',
             description='이메일과 비밀번호로 로그인합니다.',
             responses={
                 200: '로그인 성공',
                 400: '필수 필드 누락',
                 401: '인증 실패',
                 500: '서버 오류'
             })
    @api.expect(login_model)
    def post(self):
        """사용자 로그인을 처리합니다."""
        try:
            data = request.get_json()
            
            # 필수 필드 검사
            if not data or 'email' not in data or 'password' not in data:
                return {'error': 'Email and password are required'}, 400
            
            user = User.query.filter_by(email=data['email']).first()
            
            if not user or not user.check_password(data['password']):
                return {'error': 'Invalid email or password'}, 401
            
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
            
        except Exception as e:
            return {'error': str(e)}, 500 