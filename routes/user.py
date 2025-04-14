from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db, jwt
from models import User, WorkExperience, Project, Education, Award, Certificate, Skill
import logging
import traceback
import json
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
import base64
from flask_restx import Resource, Namespace
from app import api, resume_model

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

user_bp = Blueprint('user', __name__)
user_ns = Namespace('user', description='사용자 관련 API')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    work_experiences = WorkExperience.query.filter_by(user_id=user_id).all()
    projects = Project.query.filter_by(user_id=user_id).all()
    education = Education.query.filter_by(user_id=user_id).all()
    awards = Award.query.filter_by(user_id=user_id).all()
    certificates = Certificate.query.filter_by(user_id=user_id).all()
    skills = Skill.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'introduction': user.introduction,
            'phone': user.phone,
            'self_introduction': user.self_introduction,
            'portfolio': user.portfolio,
            'blog': user.blog,
            'github': user.github
        },
        'work_experiences': [{
            'id': exp.id,
            'company': exp.company,
            'department': exp.department,
            'position': exp.position,
            'is_current': exp.is_current,
            'description': exp.description,
            'start_date': exp.start_date.isoformat() if exp.start_date else None,
            'end_date': exp.end_date.isoformat() if exp.end_date else None
        } for exp in work_experiences],
        'projects': [{
            'id': proj.id,
            'name': proj.name,
            'organization': proj.organization,
            'period': proj.period,
            'description': proj.description,
            'image_url': proj.image_url,
            'is_representative': proj.is_representative
        } for proj in projects],
        'education': [{
            'id': edu.id,
            'university': edu.university,
            'major': edu.major,
            'period': edu.period,
            'description': edu.description
        } for edu in education],
        'awards': [{
            'id': award.id,
            'name': award.name,
            'period': award.period,
            'description': award.description
        } for award in awards],
        'certificates': [{
            'id': cert.id,
            'name': cert.name,
            'organization': cert.organization,
            'date': cert.date.isoformat() if cert.date else None,
            'number': cert.number
        } for cert in certificates],
        'skills': [skill.name for skill in skills]
    }), 200

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    for key, value in data.items():
        if hasattr(user, key):
            setattr(user, key, value)
    
    db.session.commit()
    return jsonify({'message': '프로필이 업데이트되었습니다.'}), 200

@user_bp.route('/work-experience', methods=['POST'])
@jwt_required()
def add_work_experience():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    new_experience = WorkExperience(
        user_id=user_id,
        company=data['company'],
        department=data.get('department'),
        position=data.get('position'),
        is_current=data.get('is_current', False),
        description=data.get('description'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date')
    )
    
    db.session.add(new_experience)
    db.session.commit()
    
    return jsonify({'message': '경력이 추가되었습니다.'}), 201

@user_bp.route('/project', methods=['POST'])
@jwt_required()
def add_project():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    new_project = Project(
        user_id=user_id,
        name=data['name'],
        organization=data.get('organization'),
        period=data.get('period'),
        description=data.get('description'),
        image_url=data.get('image_url'),
        is_representative=data.get('is_representative', False)
    )
    
    db.session.add(new_project)
    db.session.commit()
    
    return jsonify({'message': '프로젝트가 추가되었습니다.'}), 201

@user_bp.route('/skill', methods=['POST'])
@jwt_required()
def add_skill():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    new_skill = Skill(
        user_id=user_id,
        name=data['name']
    )
    
    db.session.add(new_skill)
    db.session.commit()
    
    return jsonify({'message': '기술 스택이 추가되었습니다.'}), 201

@user_ns.route('/resume')
class Resume(Resource):
    @jwt_required()
    @user_ns.doc('이력서 저장',
             description='''
             사용자의 이력서를 저장합니다.
             
             요청 데이터:
             - name: 이름 (필수)
             - email: 이메일 (필수)
             - phone: 전화번호
             - introduction: 자기소개
             - workExperience: 경력 사항 목록
               - company: 회사명 (필수)
               - position: 직책 (필수)
               - startDate: 시작일 (필수, YYYY-MM-DD)
               - endDate: 종료일 (필수, YYYY-MM-DD)
               - description: 업무 설명
             - projects: 프로젝트 목록
               - title: 프로젝트명 (필수)
               - description: 프로젝트 설명 (필수)
               - startDate: 시작일 (필수, YYYY-MM-DD)
               - endDate: 종료일 (필수, YYYY-MM-DD)
               - techStack: 사용 기술 목록
             - skills: 기술 스택 목록
             - education: 학력 목록
               - school: 학교명 (필수)
               - major: 전공 (필수)
               - degree: 학위 (필수)
               - startDate: 입학일 (필수, YYYY-MM-DD)
               - endDate: 졸업일 (필수, YYYY-MM-DD)
             ''',
             responses={
                 200: '이력서 저장 성공',
                 401: '인증 실패',
                 404: '사용자를 찾을 수 없음',
                 500: '서버 오류'
             })
    def post(self):
        """사용자의 이력서를 저장합니다."""
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user:
                return {'error': 'User not found'}, 404
            
            data = request.get_json()
            
            # 사용자 정보 업데이트
            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)
            user.phone = data.get('phone', user.phone)
            user.introduction = data.get('introduction', user.introduction)
            
            # 기존 데이터 삭제
            WorkExperience.query.filter_by(user_id=user.id).delete()
            Project.query.filter_by(user_id=user.id).delete()
            Education.query.filter_by(user_id=user.id).delete()
            
            # 경력 추가
            if 'workExperience' in data:
                for exp_data in data['workExperience']:
                    experience = WorkExperience(
                        user_id=user.id,
                        company=exp_data['company'],
                        position=exp_data['position'],
                        start_date=exp_data['startDate'],
                        end_date=exp_data['endDate'],
                        description=exp_data.get('description', '')
                    )
                    db.session.add(experience)
            
            # 프로젝트 추가
            if 'projects' in data:
                for proj_data in data['projects']:
                    project = Project(
                        user_id=user.id,
                        title=proj_data['title'],
                        description=proj_data['description'],
                        start_date=proj_data['startDate'],
                        end_date=proj_data['endDate'],
                        tech_stack=proj_data.get('techStack', [])
                    )
                    db.session.add(project)
            
            # 기술 스택 처리
            if 'skills' in data:
                user.skills = []
                for skill_name in data['skills']:
                    skill = Skill.query.filter_by(name=skill_name).first()
                    if not skill:
                        skill = Skill(name=skill_name)
                        db.session.add(skill)
                    user.skills.append(skill)
            
            # 학력 추가
            if 'education' in data:
                for edu_data in data['education']:
                    education = Education(
                        user_id=user.id,
                        school=edu_data['school'],
                        major=edu_data['major'],
                        degree=edu_data['degree'],
                        start_date=edu_data['startDate'],
                        end_date=edu_data['endDate']
                    )
                    db.session.add(education)
            
            db.session.commit()
            return {'message': 'Resume saved successfully'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500 