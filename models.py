from extensions import db
from datetime import datetime

# 사용자-기술 스택 연결 테이블
user_skills = db.Table('user_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'student' 또는 'company'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 공통 필드
    profile_image = db.Column(db.String(200))
    is_profile_public = db.Column(db.Boolean, default=True)
    
    # 수료생 전용 필드
    introduction = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    self_introduction = db.Column(db.Text)
    portfolio = db.Column(db.String(200))
    blog = db.Column(db.String(200))
    github = db.Column(db.String(200))
    course = db.Column(db.String(100))
    
    # 기업 전용 필드
    company_name = db.Column(db.String(100))
    industry = db.Column(db.String(50))
    company_size = db.Column(db.String(50))
    company_description = db.Column(db.Text)
    website = db.Column(db.String(200))
    
    # 관계 설정
    work_experiences = db.relationship('WorkExperience', backref='user', lazy=True)
    projects = db.relationship('Project', backref='user', lazy=True)
    education = db.relationship('Education', backref='user', lazy=True)
    awards = db.relationship('Award', backref='user', lazy=True)
    certificates = db.relationship('Certificate', backref='user', lazy=True)
    skills = db.relationship('Skill', secondary=user_skills, backref='users', lazy=True)

class WorkExperience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100))
    position = db.Column(db.String(100))
    is_current = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    organization = db.Column(db.String(100))
    period = db.Column(db.String(100))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    is_representative = db.Column(db.Boolean, default=False)

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    university = db.Column(db.String(100), nullable=False)
    major = db.Column(db.String(100))
    period = db.Column(db.String(100))
    description = db.Column(db.Text)

class Award(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    period = db.Column(db.String(100))
    description = db.Column(db.Text)

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    organization = db.Column(db.String(100))
    date = db.Column(db.Date)
    number = db.Column(db.String(100))

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 