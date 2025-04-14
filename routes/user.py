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

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

user_bp = Blueprint('user', __name__)

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

@user_bp.route('/resume', methods=['POST'])
@jwt_required()
def save_resume():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        logger.debug(f"Resume save request for user {current_user_id}")
        logger.debug(f"Request data: {data}")
        
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # 사용자 정보 업데이트
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
        if 'phone' in data:
            user.phone = data['phone']
        if 'introduction' in data:
            user.introduction = data['introduction']
        
        # 경력 업데이트
        if 'workExperience' in data:
            # 기존 경력 삭제
            WorkExperience.query.filter_by(user_id=current_user_id).delete()
            
            for exp in data['workExperience']:
                try:
                    work_exp = WorkExperience(
                        user_id=current_user_id,
                        company=exp['company'],
                        position=exp['position'],
                        start_date=datetime.strptime(exp['startDate'], '%Y-%m-%d'),
                        end_date=datetime.strptime(exp['endDate'], '%Y-%m-%d') if exp.get('endDate') else None,
                        description=exp.get('description', '')
                    )
                    db.session.add(work_exp)
                except Exception as e:
                    logger.error(f"Error processing work experience: {str(e)}")
                    logger.error(traceback.format_exc())
                    return jsonify({'error': 'Invalid work experience data format'}), 400
        
        # 프로젝트 업데이트
        if 'projects' in data:
            # 기존 프로젝트 삭제
            Project.query.filter_by(user_id=current_user_id).delete()
            
            for proj in data['projects']:
                try:
                    project = Project(
                        user_id=current_user_id,
                        title=proj['title'],
                        description=proj.get('description', ''),
                        start_date=datetime.strptime(proj['startDate'], '%Y-%m-%d'),
                        end_date=datetime.strptime(proj['endDate'], '%Y-%m-%d') if proj.get('endDate') else None,
                        technologies=proj.get('technologies', [])
                    )
                    
                    # 프로젝트 이미지 처리
                    if 'image' in proj and proj['image']:
                        try:
                            image_data = proj['image'].split(',')[1]  # Base64 데이터 추출
                            image_bytes = base64.b64decode(image_data)
                            
                            # 파일명 생성
                            filename = secure_filename(f"{uuid.uuid4()}.png")
                            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                            
                            # 이미지 저장
                            with open(filepath, 'wb') as f:
                                f.write(image_bytes)
                            
                            project.image_path = filename
                        except Exception as e:
                            logger.error(f"Error processing project image: {str(e)}")
                            logger.error(traceback.format_exc())
                    
                    db.session.add(project)
                except Exception as e:
                    logger.error(f"Error processing project: {str(e)}")
                    logger.error(traceback.format_exc())
                    return jsonify({'error': 'Invalid project data format'}), 400
        
        # 기술 스택 업데이트
        if 'skills' in data:
            # 기존 기술 스택 삭제
            Skill.query.filter_by(user_id=current_user_id).delete()
            
            for skill_name in data['skills']:
                try:
                    skill = Skill(
                        user_id=current_user_id,
                        name=skill_name
                    )
                    db.session.add(skill)
                except Exception as e:
                    logger.error(f"Error processing skill: {str(e)}")
                    logger.error(traceback.format_exc())
                    return jsonify({'error': 'Invalid skill data format'}), 400
        
        # 학력 업데이트
        if 'education' in data:
            # 기존 학력 삭제
            Education.query.filter_by(user_id=current_user_id).delete()
            
            for edu in data['education']:
                try:
                    education = Education(
                        user_id=current_user_id,
                        school=edu['school'],
                        degree=edu['degree'],
                        field=edu['field'],
                        start_date=datetime.strptime(edu['startDate'], '%Y-%m-%d'),
                        end_date=datetime.strptime(edu['endDate'], '%Y-%m-%d') if edu.get('endDate') else None,
                        description=edu.get('description', '')
                    )
                    db.session.add(education)
                except Exception as e:
                    logger.error(f"Error processing education: {str(e)}")
                    logger.error(traceback.format_exc())
                    return jsonify({'error': 'Invalid education data format'}), 400
        
        # 수상 업데이트
        if 'awards' in data:
            # 기존 수상 삭제
            Award.query.filter_by(user_id=current_user_id).delete()
            
            for award_data in data['awards']:
                try:
                    award = Award(
                        user_id=current_user_id,
                        title=award_data['title'],
                        organization=award_data['organization'],
                        date=datetime.strptime(award_data['date'], '%Y-%m-%d'),
                        description=award_data.get('description', '')
                    )
                    db.session.add(award)
                except Exception as e:
                    logger.error(f"Error processing award: {str(e)}")
                    logger.error(traceback.format_exc())
                    return jsonify({'error': 'Invalid award data format'}), 400
        
        # 자격증 업데이트
        if 'certificates' in data:
            # 기존 자격증 삭제
            Certificate.query.filter_by(user_id=current_user_id).delete()
            
            for cert_data in data['certificates']:
                try:
                    certificate = Certificate(
                        user_id=current_user_id,
                        name=cert_data['name'],
                        organization=cert_data['organization'],
                        issue_date=datetime.strptime(cert_data['issueDate'], '%Y-%m-%d'),
                        expiry_date=datetime.strptime(cert_data['expiryDate'], '%Y-%m-%d') if cert_data.get('expiryDate') else None,
                        description=cert_data.get('description', '')
                    )
                    db.session.add(certificate)
                except Exception as e:
                    logger.error(f"Error processing certificate: {str(e)}")
                    logger.error(traceback.format_exc())
                    return jsonify({'error': 'Invalid certificate data format'}), 400
        
        try:
            db.session.commit()
            logger.info(f"Resume saved successfully for user {current_user_id}")
            return jsonify({'message': 'Resume saved successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Database error: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({'error': 'Database error occurred'}), 500
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': 'An unexpected error occurred'}), 500 