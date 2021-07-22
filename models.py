from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from flask_login import LoginManager, UserMixin
from sqlalchemy.dialects.postgresql import JSONB


db = SQLAlchemy()
login_manager = LoginManager()

class Job_Post(db.Model, UserMixin):
    
    __tablename__ = 'Job_Post'

    id = db.Column(db.Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    job_title = db.Column(db.String(300))
    employment_type = Column(Integer)
    created_at = db.Column(db.String(200))
    location = db.Column(db.String(100))
    job_description = db.Column(db.String(800))
    skills = db.Column(JSONB)
    status = db.Column(Boolean)


    def __init__(self, user_id, job_title, employment_type, location, job_description, skills, created_at, status):
        self.user_id = user_id
        self.job_title = job_title
        self.employment_type = employment_type
        self.location = location
        self.job_description = job_description
        self.skills = skills
        self.created_at = created_at
        self.status = status

class Users(db.Model, UserMixin):
    
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    role_id = Column(Integer)
    full_name = db.Column(db.String(300))
    password = db.Column(db.String(200))
    created_at = db.Column(db.String(200))
    contact_number = db.Column(db.String(15))


    def __init__(self, email, full_name, password, created_at, contact_number, role_id):
        self.full_name = full_name
        self.email = email
        self.password = password
        self.created_at = created_at
        self.contact_number = contact_number
        self.role_id = role_id

class Recruiter(db.Model, UserMixin):
    
    __tablename__ = 'Recruiter'

    user_id = Column(Integer, ForeignKey('Users.id'))
    recruiter_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200))
    job_posted = db.Column(db.Boolean, unique=False)
    created_at = db.Column(db.String(200))


    def __init__(self, user_id, created_at, company_name, job_posted):
        self.user_id = user_id
        self.created_at = created_at
        self.company_name = company_name
        self.job_posted = job_posted


class Student(db.Model, UserMixin):
    
    __tablename__ = 'Student'

    student_id = db.Column(db.Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    created_at = db.Column(db.String(200))
    department = db.Column(db.String(200))
    applied_to_job = db.Column(db.Boolean, unique=False)


    def __init__(self, user_id, created_at, department, applied_to_job):
        self.user_id = user_id
        self.created_at = created_at
        self.department = department
        self.applied_to_job = applied_to_job



class CSO(db.Model, UserMixin):
    
    __tablename__ = 'CSO'

    cso_id = db.Column(db.Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    created_at = db.Column(db.String(200))
    campus_name = db.Column(db.String(200))

    def __init__(self, user_id, created_at, campus_name):
        self.user_id = user_id
        self.created_at = created_at
        self.campus_name = campus_name

class Employment_Type(db.Model, UserMixin):
    
    __tablename__ = 'Employment_Type'

    employment_type_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))

    def __init__(self, description):
        self.description = description

class User_Roles(db.Model, UserMixin):
    
    __tablename__ = 'User_Roles'

    user_role_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))

    def __init__(self, description):
        self.description = description

@login_manager.user_loader
def user_loader(email):
    user = Users.query.filter_by(email=email).one_or_none()
    if not user:
        return None
    else:
        return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    user = Users.query.filter_by(email=email).one_or_none()
    return user if user else None
