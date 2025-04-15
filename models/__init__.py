from flask_sqlalchemy import SQLAlchemy
from extensions import db, bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'student' or 'company'
    phone = db.Column(db.String(20))
    introduction = db.Column(db.Text)
    portfolio = db.Column(db.String(200))
    blog = db.Column(db.String(200))
    github = db.Column(db.String(200))
    
    # Student specific fields
    skills = db.relationship('Skill', secondary='user_skills', backref='users')
    course = db.Column(db.String(100))  # 수료 과정
    
    # Company specific fields
    company_name = db.Column(db.String(100))
    company_description = db.Column(db.Text)
    industry = db.Column(db.String(100))  # 산업군
    company_size = db.Column(db.String(50))  # 기업 규모
    company_website = db.Column(db.String(200))  # 기업 웹사이트
    
    # Relationships
    work_experiences = db.relationship('WorkExperience', backref='user', lazy=True)
    projects = db.relationship('Project', backref='user', lazy=True)
    education = db.relationship('Education', backref='user', lazy=True)
    awards = db.relationship('Award', backref='user', lazy=True)
    certificates = db.relationship('Certificate', backref='user', lazy=True)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class WorkExperience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100))  # 부서
    position = db.Column(db.String(100), nullable=False)
    is_current = db.Column(db.Boolean, default=False)  # 재직 여부
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    organization = db.Column(db.String(100))  # 이행기관
    portfolio_url = db.Column(db.String(200))  # 포트폴리오 링크
    image_url = db.Column(db.String(200))  # 프로젝트 이미지
    is_representative = db.Column(db.Boolean, default=False)  # 대표 프로젝트 여부
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    tech_stack = db.Column(db.JSON)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

# User-Skill association table
user_skills = db.Table('user_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    major = db.Column(db.String(100), nullable=False)
    degree = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

class Award(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)  # 수상 및 활동명
    start_date = db.Column(db.Date, nullable=False)  # 기간 시작
    end_date = db.Column(db.Date, nullable=False)  # 기간 종료
    description = db.Column(db.Text)  # 상세 내용

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)  # 자격증명
    organization = db.Column(db.String(100), nullable=False)  # 기관
    issue_date = db.Column(db.Date, nullable=False)  # 취득일
    credential_id = db.Column(db.String(100))  # 자격증번호 