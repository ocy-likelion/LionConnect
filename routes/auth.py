from flask import Blueprint, request, jsonify
from models import User
from extensions import db
from flask_jwt_extended import create_access_token
from flask_restx import Resource, Namespace, fields
import re

auth_bp = Blueprint('auth', __name__)
auth_ns = Namespace('auth', description='인증 관련 API')

# API 모델 정의
login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='사용자 이메일'),
    'password': fields.String(required=True, description='비밀번호')
})

student_fields = {
    'email': fields.String(required=True, description='사용자 이메일'),
    'password': fields.String(required=True, description='비밀번호'),
    'name': fields.String(required=True, description='이름'),
    'user_type': fields.String(required=True, description='사용자 유형 (student)'),
    'skills': fields.List(fields.String, required=True, description='기술 스택'),
    'course': fields.String(required=True, description='수료 과정')
}

company_fields = {
    'email': fields.String(required=True, description='사용자 이메일'),
    'password': fields.String(required=True, description='비밀번호'),
    'name': fields.String(required=True, description='이름'),
    'user_type': fields.String(required=True, description='사용자 유형 (company)'),
    'company_name': fields.String(required=True, description='회사명'),
    'company_description': fields.String(required=True, description='회사 소개'),
    'industry': fields.String(required=True, description='산업군'),
    'company_size': fields.String(required=True, description='기업 규모'),
    'company_website': fields.String(required=True, description='기업 웹사이트')
}

student_signup_model = auth_ns.model('StudentSignup', student_fields)
company_signup_model = auth_ns.model('CompanySignup', company_fields)

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

@auth_ns.route('/signup')
class Signup(Resource):
    @auth_ns.doc('새로운 사용자 등록',
             description='''
             새로운 사용자를 등록합니다.
             
             사용자 유형:
             - student: 학생
               - 필수 필드: email, password, name, user_type, skills, course
             - company: 기업
               - 필수 필드: email, password, name, user_type, company_name, company_description, industry, company_size, company_website
             ''',
             responses={
                 201: '회원가입 성공',
                 400: '필수 필드 누락 또는 유효하지 않은 데이터',
                 409: '이메일 중복',
                 500: '서버 오류'
             })
    @auth_ns.expect(auth_ns.model('Signup', {
        'email': fields.String(required=True),
        'password': fields.String(required=True),
        'name': fields.String(required=True),
        'user_type': fields.String(required=True),
        'skills': fields.List(fields.String),
        'course': fields.String,
        'company_name': fields.String,
        'company_description': fields.String,
        'industry': fields.String,
        'company_size': fields.String,
        'company_website': fields.String
    }))
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
            
            # 비밀번호 유효성 검사
            if not validate_password(data['password']):
                return {'error': 'Password must be at least 8 characters long and contain letters, numbers, and special characters'}, 400
            
            # 사용자 유형별 추가 필드 검사
            if data['user_type'] == 'student':
                if 'skills' not in data or not data['skills']:
                    return {'error': 'Skills are required for student'}, 400
                if 'course' not in data or not data['course']:
                    return {'error': 'Course is required for student'}, 400
            elif data['user_type'] == 'company':
                required_company_fields = ['company_name', 'company_description', 'industry', 'company_size', 'company_website']
                if not all(field in data for field in required_company_fields):
                    return {'error': f'Missing required company fields: {", ".join(required_company_fields)}'}, 400
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
                user.course = data['course']
            else:
                user.company_name = data['company_name']
                user.company_description = data['company_description']
                user.industry = data['industry']
                user.company_size = data['company_size']
                user.company_website = data['company_website']
            
            db.session.add(user)
            db.session.commit()
            
            return {'message': 'User created successfully'}, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.doc('사용자 로그인',
             description='이메일과 비밀번호로 로그인합니다.',
             responses={
                 200: '로그인 성공',
                 400: '필수 필드 누락',
                 401: '인증 실패',
                 500: '서버 오류'
             })
    @auth_ns.expect(login_model)
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
            
            access_token = create_access_token(identity=str(user.id))
            return {'access_token': access_token}, 200
            
        except Exception as e:
            return {'error': str(e)}, 500 