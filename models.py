from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from flask_login import LoginManager, UserMixin

db = SQLAlchemy()
login_manager = LoginManager()

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
