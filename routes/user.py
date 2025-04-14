from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User, WorkExperience, Project, Education, Skill
from flask_restx import Resource, Namespace, fields
import logging
import traceback
import json
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
import base64

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

user_bp = Blueprint('user', __name__)
user_ns = Namespace('user', description='사용자 관련 API')

# API 모델 정의
work_experience_model = user_ns.model('WorkExperience', {
    'company': fields.String(required=True, description='회사명'),
    'position': fields.String(required=True, description='직책'),
    'startDate': fields.String(required=True, description='시작일 (YYYY-MM-DD)'),
    'endDate': fields.String(required=True, description='종료일 (YYYY-MM-DD)'),
    'description': fields.String(description='업무 설명')
})

project_model = user_ns.model('Project', {
    'title': fields.String(required=True, description='프로젝트명'),
    'description': fields.String(required=True, description='프로젝트 설명'),
    'startDate': fields.String(required=True, description='시작일 (YYYY-MM-DD)'),
    'endDate': fields.String(required=True, description='종료일 (YYYY-MM-DD)'),
    'techStack': fields.List(fields.String, description='사용 기술')
})

education_model = user_ns.model('Education', {
    'school': fields.String(required=True, description='학교명'),
    'major': fields.String(required=True, description='전공'),
    'degree': fields.String(required=True, description='학위'),
    'startDate': fields.String(required=True, description='입학일 (YYYY-MM-DD)'),
    'endDate': fields.String(required=True, description='졸업일 (YYYY-MM-DD)')
})

profile_model = user_ns.model('Profile', {
    'name': fields.String(description='이름'),
    'email': fields.String(description='이메일'),
    'phone': fields.String(description='전화번호'),
    'introduction': fields.String(description='자기소개'),
    'portfolio': fields.String(description='포트폴리오 URL'),
    'blog': fields.String(description='블로그 URL'),
    'github': fields.String(description='GitHub URL')
})

skill_model = user_ns.model('Skill', {
    'name': fields.String(required=True, description='기술 스택 이름')
})

resume_model = user_ns.model('Resume', {
    'name': fields.String(required=True, description='이름'),
    'email': fields.String(required=True, description='이메일'),
    'phone': fields.String(description='전화번호'),
    'introduction': fields.String(description='자기소개'),
    'workExperience': fields.List(fields.Nested(work_experience_model), description='경력 사항'),
    'projects': fields.List(fields.Nested(project_model), description='프로젝트'),
    'skills': fields.List(fields.String, description='기술 스택'),
    'education': fields.List(fields.Nested(education_model), description='학력')
})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@user_ns.route('/profile')
class Profile(Resource):
    @jwt_required()
    @user_ns.doc('프로필 조회',
             description='사용자의 프로필 정보를 조회합니다.',
             responses={
                 200: '프로필 조회 성공',
                 401: '인증 실패',
                 404: '사용자를 찾을 수 없음'
             })
    def get(self):
        """사용자의 프로필 정보를 조회합니다."""
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        work_experiences = WorkExperience.query.filter_by(user_id=user_id).all()
        projects = Project.query.filter_by(user_id=user_id).all()
        education = Education.query.filter_by(user_id=user_id).all()
        
        return {
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'introduction': user.introduction,
                'phone': user.phone,
                'portfolio': user.portfolio,
                'blog': user.blog,
                'github': user.github
            },
            'work_experiences': [{
                'id': exp.id,
                'company': exp.company,
                'position': exp.position,
                'start_date': exp.start_date.isoformat() if exp.start_date else None,
                'end_date': exp.end_date.isoformat() if exp.end_date else None,
                'description': exp.description
            } for exp in work_experiences],
            'projects': [{
                'id': proj.id,
                'title': proj.title,
                'description': proj.description,
                'start_date': proj.start_date.isoformat() if proj.start_date else None,
                'end_date': proj.end_date.isoformat() if proj.end_date else None,
                'tech_stack': proj.tech_stack
            } for proj in projects],
            'education': [{
                'id': edu.id,
                'school': edu.school,
                'major': edu.major,
                'degree': edu.degree,
                'start_date': edu.start_date.isoformat() if edu.start_date else None,
                'end_date': edu.end_date.isoformat() if edu.end_date else None
            } for edu in education]
        }

    @jwt_required()
    @user_ns.doc('프로필 수정',
             description='사용자의 프로필 정보를 수정합니다.',
             responses={
                 200: '프로필 수정 성공',
                 401: '인증 실패',
                 404: '사용자를 찾을 수 없음'
             })
    @user_ns.expect(profile_model)
    def put(self):
        """사용자의 프로필 정보를 수정합니다."""
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        db.session.commit()
        return {'message': '프로필이 업데이트되었습니다.'}, 200

@user_ns.route('/work-experience')
class WorkExperienceResource(Resource):
    @jwt_required()
    @user_ns.doc('경력 추가',
             description='새로운 경력 사항을 추가합니다.',
             responses={
                 201: '경력 추가 성공',
                 401: '인증 실패',
                 400: '잘못된 요청'
             })
    @user_ns.expect(work_experience_model)
    def post(self):
        """새로운 경력 사항을 추가합니다."""
        user_id = get_jwt_identity()
        data = request.get_json()
        
        new_experience = WorkExperience(
            user_id=user_id,
            company=data['company'],
            position=data['position'],
            start_date=data['startDate'],
            end_date=data['endDate'],
            description=data.get('description', '')
        )
        
        db.session.add(new_experience)
        db.session.commit()
        
        return {'message': '경력이 추가되었습니다.'}, 201

@user_ns.route('/project')
class ProjectResource(Resource):
    @jwt_required()
    @user_ns.doc('프로젝트 추가',
             description='새로운 프로젝트를 추가합니다.',
             responses={
                 201: '프로젝트 추가 성공',
                 401: '인증 실패',
                 400: '잘못된 요청'
             })
    @user_ns.expect(project_model)
    def post(self):
        """새로운 프로젝트를 추가합니다."""
        user_id = get_jwt_identity()
        data = request.get_json()
        
        new_project = Project(
            user_id=user_id,
            title=data['title'],
            description=data['description'],
            start_date=data['startDate'],
            end_date=data['endDate'],
            tech_stack=data.get('techStack', [])
        )
        
        db.session.add(new_project)
        db.session.commit()
        
        return {'message': '프로젝트가 추가되었습니다.'}, 201

@user_ns.route('/skill')
class SkillResource(Resource):
    @jwt_required()
    @user_ns.doc('기술 스택 추가',
             description='새로운 기술 스택을 추가합니다.',
             responses={
                 201: '기술 스택 추가 성공',
                 401: '인증 실패',
                 400: '잘못된 요청'
             })
    @user_ns.expect(skill_model)
    def post(self):
        """새로운 기술 스택을 추가합니다."""
        user_id = get_jwt_identity()
        data = request.get_json()
        
        new_skill = Skill(
            user_id=user_id,
            name=data['name']
        )
        
        db.session.add(new_skill)
        db.session.commit()
        
        return {'message': '기술 스택이 추가되었습니다.'}, 201

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
    @user_ns.expect(resume_model)
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