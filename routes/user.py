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
    @user_ns.doc('프로필 조회',
             description='사용자의 프로필 정보를 조회합니다.',
             responses={
                 200: '프로필 조회 성공',
                 401: '인증 실패',
                 404: '사용자를 찾을 수 없음',
                 500: '서버 오류'
             })
    @jwt_required()
    def get(self):
        """사용자의 프로필 정보를 조회합니다."""
        try:
            # 토큰에서 사용자 ID 가져오기
            current_user_id = get_jwt_identity()
            print(f"토큰에서 가져온 user_id: {current_user_id}, 타입: {type(current_user_id)}")  # 디버깅용 로그
            
            # 데이터베이스에서 사용자 조회
            user = User.query.get(current_user_id)
            print(f"조회된 사용자: {user}, 타입: {type(user)}")  # 디버깅용 로그
            
            if not user:
                print("사용자를 찾을 수 없음")  # 디버깅용 로그
                return {'message': 'User not found'}, 404
                
            try:
                # 관련 데이터 조회
                work_experiences = WorkExperience.query.filter_by(user_id=current_user_id).all()
                projects = Project.query.filter_by(user_id=current_user_id).all()
                education = Education.query.filter_by(user_id=current_user_id).all()
                awards = Award.query.filter_by(user_id=current_user_id).all()
                certificates = Certificate.query.filter_by(user_id=current_user_id).all()
                skills = user.skills  # User 모델의 relationship을 통해 skills 조회
                
                print(f"조회된 데이터 수: work_experiences={len(work_experiences)}, projects={len(projects)}, education={len(education)}, awards={len(awards)}, certificates={len(certificates)}, skills={len(skills)}")  # 디버깅용 로그
                
                # 응답 데이터 구성
                response_data = {
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'name': user.name,
                        'introduction': user.introduction,
                        'phone': user.phone,
                        'portfolio': user.portfolio,
                        'blog': user.blog,
                        'github': user.github,
                        'user_type': user.user_type  # user_type 추가
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
                    } for cert in certificates],
                    'skills': [{
                        'id': skill.id,
                        'name': skill.name,
                        'level': skill.level
                    } for skill in skills]
                }
                
                return response_data, 200
                
            except Exception as e:
                logger.error(f"Error in get_profile: {str(e)}")
                return {'error': str(e)}, 500
                
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
             - name: 이름
             - email: 이메일
             - phone: 전화번호
             - introduction: 자기소개
             - portfolio: 포트폴리오 URL
             - blog: 블로그 URL
             - github: GitHub URL
             - workExperience: 경력 사항 목록
             - projects: 프로젝트 목록
             - skills: 기술 스택 목록
             - education: 학력 목록
             - awards: 수상 목록
             - certificates: 자격증 목록
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
            print(f"[DEBUG] 토큰에서 가져온 user_id: {current_user_id}, 타입: {type(current_user_id)}")
            
            user = User.query.get(current_user_id)
            print(f"[DEBUG] 조회된 사용자: {user}, 타입: {type(user)}")
            
            if not user:
                print("[DEBUG] 사용자를 찾을 수 없음")
                return {'message': 'User not found'}, 404
            
            data = request.get_json()
            print(f"[DEBUG] 받은 요청 데이터: {data}")
            
            try:
                # 기본 정보 업데이트 (이메일 제외)
                user.name = data.get('name', user.name)
                user.phone = data.get('phone', user.phone)
                user.introduction = data.get('introduction', user.introduction)
                user.portfolio = data.get('portfolio', user.portfolio)
                user.blog = data.get('blog', user.blog)
                user.github = data.get('github', user.github)
                
                print("[DEBUG] 기본 정보 업데이트 완료")
                
                # 기존 데이터 삭제
                WorkExperience.query.filter_by(user_id=current_user_id).delete()
                Project.query.filter_by(user_id=current_user_id).delete()
                Education.query.filter_by(user_id=current_user_id).delete()
                Award.query.filter_by(user_id=current_user_id).delete()
                Certificate.query.filter_by(user_id=current_user_id).delete()
                
                print("[DEBUG] 기존 데이터 삭제 완료")
                
                # 경력 사항 저장
                for exp_data in data.get('workExperience', []):
                    print(f"[DEBUG] 경력 데이터 처리: {exp_data}")
                    try:
                        exp = WorkExperience(
                            user_id=current_user_id,
                            company=exp_data['company'],
                            department=exp_data.get('department'),
                            position=exp_data.get('position'),
                            is_current=exp_data.get('is_current', False),
                            description=exp_data.get('description'),
                            start_date=datetime.strptime(exp_data['startDate'], '%Y-%m-%d').date() if exp_data.get('startDate') else None,
                            end_date=datetime.strptime(exp_data['endDate'], '%Y-%m-%d').date() if exp_data.get('endDate') else None
                        )
                        db.session.add(exp)
                        print(f"[DEBUG] 경력 추가: {exp.company}")
                    except Exception as e:
                        print(f"[DEBUG] 경력 데이터 처리 중 오류: {str(e)}")
                        raise
                
                # 프로젝트 저장
                for proj_data in data.get('projects', []):
                    print(f"[DEBUG] 프로젝트 데이터 처리: {proj_data}")
                    try:
                        proj = Project(
                            user_id=current_user_id,
                            title=proj_data['title'],
                            organization=proj_data.get('organization'),
                            description=proj_data.get('description'),
                            portfolio_url=proj_data.get('portfolio_url'),
                            image_url=proj_data.get('image_url'),
                            is_representative=proj_data.get('is_representative', False),
                            start_date=datetime.strptime(proj_data['startDate'], '%Y-%m-%d').date() if proj_data.get('startDate') else None,
                            end_date=datetime.strptime(proj_data['endDate'], '%Y-%m-%d').date() if proj_data.get('endDate') else None,
                            tech_stack=proj_data.get('techStack', [])
                        )
                        db.session.add(proj)
                        print(f"[DEBUG] 프로젝트 추가: {proj.title}")
                    except Exception as e:
                        print(f"[DEBUG] 프로젝트 데이터 처리 중 오류: {str(e)}")
                        raise
                
                # 학력 저장
                for edu_data in data.get('education', []):
                    print(f"[DEBUG] 학력 데이터 처리: {edu_data}")
                    try:
                        edu = Education(
                            user_id=current_user_id,
                            school=edu_data['school'],
                            major=edu_data.get('major'),
                            degree=edu_data.get('degree'),
                            start_date=datetime.strptime(edu_data['startDate'], '%Y-%m-%d').date() if edu_data.get('startDate') else None,
                            end_date=datetime.strptime(edu_data['endDate'], '%Y-%m-%d').date() if edu_data.get('endDate') else None
                        )
                        db.session.add(edu)
                        print(f"[DEBUG] 학력 추가: {edu.school}")
                    except Exception as e:
                        print(f"[DEBUG] 학력 데이터 처리 중 오류: {str(e)}")
                        raise
                
                # 수상 내역 저장
                for award_data in data.get('awards', []):
                    print(f"[DEBUG] 수상 데이터 처리: {award_data}")
                    try:
                        award = Award(
                            user_id=current_user_id,
                            title=award_data['title'],
                            start_date=datetime.strptime(award_data['startDate'], '%Y-%m-%d').date() if award_data.get('startDate') else None,
                            end_date=datetime.strptime(award_data['endDate'], '%Y-%m-%d').date() if award_data.get('endDate') else None,
                            description=award_data.get('description')
                        )
                        db.session.add(award)
                        print(f"[DEBUG] 수상 추가: {award.title}")
                    except Exception as e:
                        print(f"[DEBUG] 수상 데이터 처리 중 오류: {str(e)}")
                        raise
                
                # 자격증 저장
                for cert_data in data.get('certificates', []):
                    print(f"[DEBUG] 자격증 데이터 처리: {cert_data}")
                    try:
                        cert = Certificate(
                            user_id=current_user_id,
                            name=cert_data['title'],
                            organization=cert_data.get('organization'),
                            issue_date=datetime.strptime(cert_data['issueDate'], '%Y-%m-%d').date() if cert_data.get('issueDate') else None,
                            credential_id=cert_data.get('credential_id')
                        )
                        db.session.add(cert)
                        print(f"[DEBUG] 자격증 추가: {cert.name}")
                    except Exception as e:
                        print(f"[DEBUG] 자격증 데이터 처리 중 오류: {str(e)}")
                        raise
                
                # 기술 스택 저장
                print(f"[DEBUG] 기술 스택 처리: {data.get('skills', [])}")
                try:
                    for skill_name in data.get('skills', []):
                        skill = Skill.query.filter_by(name=skill_name).first()
                        if not skill:
                            skill = Skill(name=skill_name)
                            db.session.add(skill)
                            db.session.flush()  # ID 생성을 위해 flush
                        user.skills.append(skill)
                    print("[DEBUG] 기술 스택 추가 완료")
                except Exception as e:
                    print(f"[DEBUG] 기술 스택 처리 중 오류: {str(e)}")
                    raise
                
                db.session.commit()
                print("[DEBUG] 모든 데이터 저장 완료")
                
                return {'message': 'Resume saved successfully'}, 200
                
            except Exception as e:
                db.session.rollback()
                print(f"[DEBUG] 데이터 저장 중 오류 발생: {str(e)}")
                logger.error(f"Error saving resume: {str(e)}")
                return {'error': str(e)}, 500
                
        except Exception as e:
            print(f"[DEBUG] 전체 프로세스 중 오류 발생: {str(e)}")
            logger.error(f"Error in save_resume: {str(e)}")
            return {'error': str(e)}, 500 