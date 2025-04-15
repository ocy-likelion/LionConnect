from flask import Blueprint, request, jsonify
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, db

company_bp = Blueprint('company', __name__)
company_ns = Namespace('company', description='기업 관련 API')

# API 모델 정의
company_profile_model = company_ns.model('CompanyProfile', {
    'company_name': fields.String(required=True, description='회사명'),
    'company_description': fields.String(required=True, description='회사 소개'),
    'industry': fields.String(required=True, description='산업군'),
    'company_size': fields.String(required=True, description='기업 규모'),
    'company_website': fields.String(required=True, description='기업 웹사이트')
})

@company_ns.route('/profile')
class CompanyProfile(Resource):
    @company_ns.doc('기업 프로필 조회',
                description='기업 프로필 정보를 조회합니다.',
                responses={
                    200: '조회 성공',
                    401: '인증 실패',
                    404: '프로필 없음',
                    500: '서버 오류'
                })
    @jwt_required()
    def get(self):
        """기업 프로필 정보를 조회합니다."""
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user or user.user_type != 'company':
                return {'error': 'Unauthorized access'}, 401
            
            return {
                'company_name': user.company_name,
                'company_description': user.company_description,
                'industry': user.industry,
                'company_size': user.company_size,
                'company_website': user.company_website
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

    @company_ns.doc('기업 프로필 수정',
                description='기업 프로필 정보를 수정합니다.',
                responses={
                    200: '수정 성공',
                    400: '잘못된 요청',
                    401: '인증 실패',
                    500: '서버 오류'
                })
    @company_ns.expect(company_profile_model)
    @jwt_required()
    def put(self):
        """기업 프로필 정보를 수정합니다."""
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user or user.user_type != 'company':
                return {'error': 'Unauthorized access'}, 401
            
            data = request.get_json()
            
            # 필수 필드 검사
            required_fields = ['company_name', 'company_description', 'industry', 'company_size', 'company_website']
            if not all(field in data for field in required_fields):
                return {'error': 'Missing required fields'}, 400
            
            # 프로필 정보 업데이트
            user.company_name = data['company_name']
            user.company_description = data['company_description']
            user.industry = data['industry']
            user.company_size = data['company_size']
            user.company_website = data['company_website']
            
            db.session.commit()
            return {'message': 'Company profile updated successfully'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500 