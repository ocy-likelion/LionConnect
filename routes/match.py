from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Match, User, Skill
from sqlalchemy import and_

match_bp = Blueprint('match', __name__)

@match_bp.route('/suggestions', methods=['GET'])
@jwt_required()
def get_match_suggestions():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    # 사용자의 기술 스택 가져오기
    user_skills = [skill.name for skill in Skill.query.filter_by(user_id=user_id).all()]
    
    # 다른 사용자들의 기술 스택과 매칭
    suggestions = []
    other_users = User.query.filter(User.id != user_id).all()
    
    for other_user in other_users:
        other_skills = [skill.name for skill in Skill.query.filter_by(user_id=other_user.id).all()]
        matching_skills = set(user_skills) & set(other_skills)
        
        if matching_skills:
            suggestions.append({
                'user': {
                    'id': other_user.id,
                    'name': other_user.name,
                    'introduction': other_user.introduction
                },
                'matching_skills': list(matching_skills)
            })
    
    return jsonify({'suggestions': suggestions}), 200

@match_bp.route('/request', methods=['POST'])
@jwt_required()
def request_match():
    user_id = get_jwt_identity()
    data = request.get_json()
    receiver_id = data['receiver_id']
    
    # 이미 존재하는 매칭 요청 확인
    existing_match = Match.query.filter(
        and_(
            Match.requester_id == user_id,
            Match.receiver_id == receiver_id,
            Match.status == 'pending'
        )
    ).first()
    
    if existing_match:
        return jsonify({'error': '이미 매칭 요청을 보냈습니다.'}), 400
    
    new_match = Match(
        requester_id=user_id,
        receiver_id=receiver_id
    )
    
    db.session.add(new_match)
    db.session.commit()
    
    return jsonify({'message': '매칭 요청이 전송되었습니다.'}), 201

@match_bp.route('/requests', methods=['GET'])
@jwt_required()
def get_match_requests():
    user_id = get_jwt_identity()
    
    # 받은 매칭 요청
    received_requests = Match.query.filter_by(receiver_id=user_id, status='pending').all()
    # 보낸 매칭 요청
    sent_requests = Match.query.filter_by(requester_id=user_id).all()
    
    return jsonify({
        'received_requests': [{
            'id': request.id,
            'requester': {
                'id': request.requester.id,
                'name': request.requester.name
            },
            'created_at': request.created_at.isoformat()
        } for request in received_requests],
        'sent_requests': [{
            'id': request.id,
            'receiver': {
                'id': request.receiver.id,
                'name': request.receiver.name
            },
            'status': request.status,
            'created_at': request.created_at.isoformat()
        } for request in sent_requests]
    }), 200

@match_bp.route('/<int:match_id>/respond', methods=['POST'])
@jwt_required()
def respond_to_match(match_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    response = data['response']  # 'accept' or 'reject'
    
    match = Match.query.get_or_404(match_id)
    
    if match.receiver_id != user_id:
        return jsonify({'error': '응답 권한이 없습니다.'}), 403
    
    if match.status != 'pending':
        return jsonify({'error': '이미 처리된 요청입니다.'}), 400
    
    match.status = 'accepted' if response == 'accept' else 'rejected'
    db.session.commit()
    
    return jsonify({'message': f'매칭 요청이 {response}되었습니다.'}), 200 