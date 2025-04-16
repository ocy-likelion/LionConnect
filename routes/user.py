from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User, WorkExperience, Project, Education, Skill, Award, Certificate
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
    'department': fields.String(required=True, description='부서'),
    'position': fields.String(required=True, description='직책'),
    'is_current': fields.Boolean(description='재직 여부'),
    'startDate': fields.String(required=True, description='시작일 (YYYY-MM-DD)'),
    'endDate': fields.String(required=True, description='종료일 (YYYY-MM-DD)'),
    'description': fields.String(description='업무 설명')
})

project_model = user_ns.model('Project', {
    'title': fields.String(required=True, description='프로젝트명'),
    'description': fields.String(required=True, description='프로젝트 설명'),
    'organization': fields.String(description='이행기관'),
    'portfolio_url': fields.String(description='포트폴리오 링크'),
    'image': fields.String(description='프로젝트 이미지 (Base64)'),
    'is_representative': fields.Boolean(description='대표 프로젝트 여부'),
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

award_model = user_ns.model('Award', {
    'title': fields.String(required=True, description='수상 및 활동명'),
    'startDate': fields.String(required=True, description='시작일 (YYYY-MM-DD)'),
    'endDate': fields.String(required=True, description='종료일 (YYYY-MM-DD)'),
    'description': fields.String(description='상세 내용')
})

certificate_model = user_ns.model('Certificate', {
    'title': fields.String(required=True, description='자격증명'),
    'organization': fields.String(required=True, description='기관'),
    'issueDate': fields.String(required=True, description='취득일 (YYYY-MM-DD)'),
    'credential_id': fields.String(description='자격증번호')
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
    'portfolio': fields.String(description='포트폴리오 URL'),
    'blog': fields.String(description='블로그 URL'),
    'github': fields.String(description='GitHub URL'),
    'workExperience': fields.List(fields.Nested(work_experience_model), description='경력 사항'),
    'projects': fields.List(fields.Nested(project_model), description='프로젝트'),
    'skills': fields.List(fields.String, description='기술 스택'),
    'education': fields.List(fields.Nested(education_model), description='학력'),
    'awards': fields.List(fields.Nested(award_model), description='수상 및 활동'),
    'certificates': fields.List(fields.Nested(certificate_model), description='자격증')
})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_base64_image(base64_string, user_id):
    try:
        # Base64 문자열에서 데이터 부분만 추출
        if ',' in base64_string:
            header, base64_string = base64_string.split(',', 1)
        
        # 이미지 데이터를 디코드
        image_data = base64.b64decode(base64_string)
        
        # 파일 이름 생성
        filename = f"{user_id}_{uuid.uuid4()}.jpg"
        
        # 파일 저장
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        with open(file_path, 'wb') as f:
            f.write(image_data)
        
        # 파일의 URL 반환
        return f"/uploads/{filename}"
    except Exception as e:
        logger.error(f"Error saving base64 image: {str(e)}")
        return None

@user_ns.route('/profile')
class Profile(Resource):
    @jwt_required()
    @user_ns.doc('프로필 조회',
             description='사용자의 프로필 정보를 조회합니다.',
             responses={
                 200: '프로필 조회 성공',
                 401: '인증 실패',
                 404: '사용자를 찾을 수 없음',
                 500: '서버 오류'
             })
    def get(self):
        """사용자의 프로필 정보를 조회합니다."""
        try:
            # 토큰에서 사용자 ID 가져오기 (문자열 상태로 유지)
            current_user_id = get_jwt_identity()
            print(f"토큰에서 가져온 user_id (문자열): {current_user_id}")  # 디버깅용 로그
            
            # 문자열 ID를 정수로 변환하여 데이터베이스 조회
            user = User.query.get(int(current_user_id))
            print(f"조회된 사용자: {user}")  # 디버깅용 로그
            
            if not user:
                return {'message': 'User not found'}, 404
            
            work_experiences = WorkExperience.query.filter_by(user_id=int(current_user_id)).all()
            projects = Project.query.filter_by(user_id=int(current_user_id)).all()
            education = Education.query.filter_by(user_id=int(current_user_id)).all()
            awards = Award.query.filter_by(user_id=int(current_user_id)).all()
            certificates = Certificate.query.filter_by(user_id=int(current_user_id)).all()
            
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
                    'department': exp.department,
                    'position': exp.position,
                    'is_current': exp.is_current,
                    'start_date': exp.start_date.isoformat() if exp.start_date else None,
                    'end_date': exp.end_date.isoformat() if exp.end_date else None,
                    'description': exp.description
                } for exp in work_experiences],
                'projects': [{
                    'id': proj.id,
                    'title': proj.title,
                    'description': proj.description,
                    'organization': proj.organization,
                    'portfolio_url': proj.portfolio_url,
                    'image_url': proj.image_url,
                    'is_representative': proj.is_representative,
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
                } for edu in education],
                'awards': [{
                    'id': award.id,
                    'title': award.title,
                    'start_date': award.start_date.isoformat() if award.start_date else None,
                    'end_date': award.end_date.isoformat() if award.end_date else None,
                    'description': award.description
                } for award in awards],
                'certificates': [{
                    'id': cert.id,
                    'title': cert.title,
                    'organization': cert.organization,
                    'issue_date': cert.issue_date.isoformat() if cert.issue_date else None,
                    'credential_id': cert.credential_id
                } for cert in certificates]
            }
        except Exception as e:
            logger.error(f"Error in get_profile: {str(e)}")
            return {'error': str(e)}, 500

    @jwt_required()
    @user_ns.doc('프로필 수정',
             description='사용자의 프로필 정보를 수정합니다.',
             responses={
                 200: '프로필 수정 성공',
                 401: '인증 실패',
                 404: '사용자를 찾을 수 없음',
                 500: '서버 오류'
             })
    @user_ns.expect(profile_model)
    def put(self):
        """사용자의 프로필 정보를 수정합니다."""
        try:
            user_id = get_jwt_identity()
            user = User.query.get_or_404(user_id)
            data = request.get_json()
            
            for key, value in data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            
            db.session.commit()
            return {'message': '프로필이 업데이트되었습니다.'}, 200
        except Exception as e:
            logger.error(f"Error in update_profile: {str(e)}")
            return {'error': str(e)}, 500

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
            department=data['department'],
            position=data['position'],
            is_current=data['is_current'],
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
            organization=data.get('organization'),
            portfolio_url=data.get('portfolio_url'),
            image_url=data.get('image'),
            is_representative=data.get('is_representative', False),
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
             - portfolio: 포트폴리오 URL
             - blog: 블로그 URL
             - github: GitHub URL
             - workExperience: 경력 사항 목록
               - company: 회사명 (필수)
               - department: 부서 (필수)
               - position: 직책 (필수)
               - is_current: 재직 여부
               - startDate: 시작일 (필수, YYYY-MM-DD)
               - endDate: 종료일 (필수, YYYY-MM-DD)
               - description: 업무 설명
             - projects: 프로젝트 목록
               - title: 프로젝트명 (필수)
               - description: 프로젝트 설명 (필수)
               - organization: 이행기관
               - portfolio_url: 포트폴리오 링크
               - image: 프로젝트 이미지 (Base64)
               - is_representative: 대표 프로젝트 여부
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
             - awards: 수상 및 활동 목록
               - title: 수상 및 활동명 (필수)
               - startDate: 시작일 (필수, YYYY-MM-DD)
               - endDate: 종료일 (필수, YYYY-MM-DD)
               - description: 상세 내용
             - certificates: 자격증 목록
               - title: 자격증명 (필수)
               - organization: 기관 (필수)
               - issueDate: 취득일 (필수, YYYY-MM-DD)
               - credential_id: 자격증번호
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
            user.portfolio = data.get('portfolio', user.portfolio)
            user.blog = data.get('blog', user.blog)
            user.github = data.get('github', user.github)
            
            # 기존 데이터 삭제
            WorkExperience.query.filter_by(user_id=user.id).delete()
            Project.query.filter_by(user_id=user.id).delete()
            Education.query.filter_by(user_id=user.id).delete()
            Award.query.filter_by(user_id=user.id).delete()
            Certificate.query.filter_by(user_id=user.id).delete()
            
            # 경력 추가
            if 'workExperience' in data:
                for exp_data in data['workExperience']:
                    experience = WorkExperience(
                        user_id=user.id,
                        company=exp_data['company'],
                        department=exp_data['department'],
                        position=exp_data['position'],
                        is_current=exp_data['is_current'],
                        start_date=exp_data['startDate'],
                        end_date=exp_data['endDate'],
                        description=exp_data.get('description', '')
                    )
                    db.session.add(experience)
            
            # 프로젝트 추가
            if 'projects' in data:
                for proj_data in data['projects']:
                    # 이미지 처리
                    image_url = None
                    if 'image' in proj_data and proj_data['image']:
                        image_url = save_base64_image(proj_data['image'], user.id)
                    
                    project = Project(
                        user_id=user.id,
                        title=proj_data['title'],
                        description=proj_data['description'],
                        organization=proj_data.get('organization'),
                        portfolio_url=proj_data.get('portfolio_url'),
                        image_url=image_url,
                        is_representative=proj_data.get('is_representative', False),
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
            
            # 수상 및 활동 추가
            if 'awards' in data:
                for award_data in data['awards']:
                    award = Award(
                        user_id=user.id,
                        title=award_data['title'],
                        start_date=award_data['startDate'],
                        end_date=award_data['endDate'],
                        description=award_data.get('description', '')
                    )
                    db.session.add(award)
            
            # 자격증 추가
            if 'certificates' in data:
                for cert_data in data['certificates']:
                    certificate = Certificate(
                        user_id=user.id,
                        title=cert_data['title'],
                        organization=cert_data['organization'],
                        issue_date=cert_data['issueDate'],
                        credential_id=cert_data.get('credential_id')
                    )
                    db.session.add(certificate)
            
            db.session.commit()
            return {'message': 'Resume saved successfully'}, 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving resume: {str(e)}\n{traceback.format_exc()}")
            return {'error': str(e)}, 500 