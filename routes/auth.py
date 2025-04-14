from flask import Blueprint, request, jsonify
from models import User, Skill
from extensions import db, bcrypt, jwt, create_access_token
from flask_restx import Resource, Namespace
import re
from app import api, user_model, login_model

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
    @api.doc('회원가입',
             description='''
             새로운 사용자를 등록합니다.
             
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
             - 201: 회원가입 성공
             - 400: 필수 필드 누락 또는 비밀번호 유효성 검사 실패
             - 500: 서버 오류
             ''')
    @api.expect(user_model)
    @api.response(201, '회원가입 성공')
    @api.response(400, '잘못된 요청')
    @api.response(500, '서버 오류')
    def post(self):
        """새로운 사용자를 등록합니다."""
        try:
            data = request.get_json()
            
            # 필수 필드 확인
            required_fields = ['email', 'password', 'name', 'user_type']
            for field in required_fields:
                if field not in data:
                    return {'error': f'{field} is required'}, 400
            
            # 이메일 중복 확인
            if User.query.filter_by(email=data['email']).first():
                return {'error': 'Email already exists'}, 400
            
            # 비밀번호 유효성 검사
            if not validate_password(data['password']):
                return {'error': 'Password must be at least 8 characters long and contain at least one letter, one number, and one special character'}, 400
            
            # 비밀번호 해시화
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            
            # 사용자 생성
            user = User(
                email=data['email'],
                password=hashed_password,
                name=data['name'],
                user_type=data['user_type']
            )
            
            # 사용자 타입에 따른 추가 필드 설정
            if data['user_type'] == 'student':
                user.course = data.get('course')
                user.skills = data.get('skills', [])
                user.portfolio = data.get('portfolio')
                
                # 기술 스택 처리
                if 'skills' in data:
                    for skill_name in data['skills']:
                        skill = Skill.query.filter_by(name=skill_name).first()
                        if not skill:
                            skill = Skill(name=skill_name)
                            db.session.add(skill)
                        user.skills.append(skill)
            
            elif data['user_type'] == 'company':
                user.company_name = data.get('company_name')
                user.industry = data.get('industry')
                user.company_size = data.get('company_size')
                user.company_location = data.get('company_location')
            
            db.session.add(user)
            db.session.commit()
            
            return {'message': 'User created successfully'}, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

@api.route('/login')
class Login(Resource):
    @api.doc('로그인',
             description='''
             사용자 로그인을 처리합니다.
             
             요청 데이터:
             - email: 사용자 이메일 (필수)
             - password: 비밀번호 (필수)
             
             응답:
             - 200: 로그인 성공, JWT 토큰 반환
             - 400: 필수 필드 누락
             - 401: 잘못된 이메일 또는 비밀번호
             - 500: 서버 오류
             ''')
    @api.expect(login_model)
    @api.response(200, '로그인 성공')
    @api.response(400, '잘못된 요청')
    @api.response(401, '인증 실패')
    @api.response(500, '서버 오류')
    def post(self):
        """사용자 로그인을 처리합니다."""
        try:
            data = request.get_json()
            
            # 필수 필드 확인
            if not data.get('email') or not data.get('password'):
                return {'error': 'Email and password are required'}, 400
            
            # 사용자 확인
            user = User.query.filter_by(email=data['email']).first()
            if not user or not bcrypt.check_password_hash(user.password, data['password']):
                return {'error': 'Invalid email or password'}, 401
            
            # JWT 토큰 생성
            token = create_access_token(identity=user.id)
            return {'token': token}, 200
            
        except Exception as e:
            return {'error': str(e)}, 500 