from flask import Blueprint, request, jsonify
from models import User, Skill
from extensions import db, bcrypt, jwt, create_access_token
import re

auth_bp = Blueprint('auth', __name__)

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

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
        # 필수 필드 확인
        required_fields = ['email', 'password', 'name', 'user_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # 이메일 중복 확인
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # 비밀번호 유효성 검사
        if not validate_password(data['password']):
            return jsonify({'error': 'Password must be at least 8 characters long and contain at least one letter, one number, and one special character'}), 400
        
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
        
        return jsonify({'message': 'User created successfully'}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # 필수 필드 확인
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # 사용자 확인
        user = User.query.filter_by(email=data['email']).first()
        if not user or not bcrypt.check_password_hash(user.password, data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # JWT 토큰 생성
        token = create_access_token(identity=user.id)
        return jsonify({'token': token}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 