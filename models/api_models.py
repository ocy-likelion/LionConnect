from flask_restx import fields

def create_api_models(api):
    # 로그인 모델
    login_model = api.model('Login', {
        'email': fields.String(required=True, description='사용자 이메일'),
        'password': fields.String(required=True, description='비밀번호')
    })

    # 회원가입 모델
    signup_model = api.model('Signup', {
        'email': fields.String(required=True, description='사용자 이메일'),
        'password': fields.String(required=True, description='비밀번호'),
        'name': fields.String(required=True, description='이름'),
        'user_type': fields.String(required=True, description='사용자 유형 (student/company)'),
        'skills': fields.List(fields.String, description='기술 스택 (학생인 경우)'),
        'company_name': fields.String(description='회사명 (기업인 경우)'),
        'company_description': fields.String(description='회사 소개 (기업인 경우)')
    })

    # 경력 모델
    work_experience_model = api.model('WorkExperience', {
        'company': fields.String(required=True, description='회사명'),
        'position': fields.String(required=True, description='직책'),
        'startDate': fields.String(required=True, description='시작일 (YYYY-MM-DD)'),
        'endDate': fields.String(required=True, description='종료일 (YYYY-MM-DD)'),
        'description': fields.String(description='업무 설명')
    })

    # 프로젝트 모델
    project_model = api.model('Project', {
        'title': fields.String(required=True, description='프로젝트명'),
        'description': fields.String(required=True, description='프로젝트 설명'),
        'startDate': fields.String(required=True, description='시작일 (YYYY-MM-DD)'),
        'endDate': fields.String(required=True, description='종료일 (YYYY-MM-DD)'),
        'techStack': fields.List(fields.String, description='사용 기술')
    })

    # 학력 모델
    education_model = api.model('Education', {
        'school': fields.String(required=True, description='학교명'),
        'major': fields.String(required=True, description='전공'),
        'degree': fields.String(required=True, description='학위'),
        'startDate': fields.String(required=True, description='입학일 (YYYY-MM-DD)'),
        'endDate': fields.String(required=True, description='졸업일 (YYYY-MM-DD)')
    })

    # 이력서 모델
    resume_model = api.model('Resume', {
        'name': fields.String(required=True, description='이름'),
        'email': fields.String(required=True, description='이메일'),
        'phone': fields.String(description='전화번호'),
        'introduction': fields.String(description='자기소개'),
        'workExperience': fields.List(fields.Nested(work_experience_model), description='경력 사항'),
        'projects': fields.List(fields.Nested(project_model), description='프로젝트'),
        'skills': fields.List(fields.String, description='기술 스택'),
        'education': fields.List(fields.Nested(education_model), description='학력')
    })

    return {
        'login_model': login_model,
        'signup_model': signup_model,
        'resume_model': resume_model
    } 