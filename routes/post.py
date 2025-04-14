from flask import Blueprint, request, jsonify
from extensions import db
from models import Post, Comment, User
from flask_jwt_extended import jwt_required, get_jwt_identity

post_bp = Blueprint('post', __name__)

@post_bp.route('', methods=['GET'])
def get_posts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'posts': [{
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'user': {
                'id': post.user.id,
                'name': post.user.name
            },
            'created_at': post.created_at.isoformat(),
            'likes': post.likes
        } for post in posts.items],
        'total': posts.total,
        'pages': posts.pages,
        'current_page': posts.page
    }), 200

@post_bp.route('', methods=['POST'])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    new_post = Post(
        user_id=user_id,
        title=data['title'],
        content=data['content']
    )
    
    db.session.add(new_post)
    db.session.commit()
    
    return jsonify({'message': '게시글이 작성되었습니다.', 'post_id': new_post.id}), 201

@post_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()
    
    return jsonify({
        'post': {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'user': {
                'id': post.user.id,
                'name': post.user.name
            },
            'created_at': post.created_at.isoformat(),
            'likes': post.likes
        },
        'comments': [{
            'id': comment.id,
            'content': comment.content,
            'user': {
                'id': comment.user.id,
                'name': comment.user.name
            },
            'created_at': comment.created_at.isoformat()
        } for comment in comments]
    }), 200

@post_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)
    
    if post.user_id != user_id:
        return jsonify({'error': '수정 권한이 없습니다.'}), 403
    
    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    
    db.session.commit()
    return jsonify({'message': '게시글이 수정되었습니다.'}), 200

@post_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)
    
    if post.user_id != user_id:
        return jsonify({'error': '삭제 권한이 없습니다.'}), 403
    
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': '게시글이 삭제되었습니다.'}), 200

@post_bp.route('/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(post_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    new_comment = Comment(
        post_id=post_id,
        user_id=user_id,
        content=data['content']
    )
    
    db.session.add(new_comment)
    db.session.commit()
    
    return jsonify({'message': '댓글이 작성되었습니다.', 'comment_id': new_comment.id}), 201

@post_bp.route('/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.likes += 1
    db.session.commit()
    return jsonify({'message': '좋아요가 추가되었습니다.', 'likes': post.likes}), 200 