from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean
from flask_login import LoginManager, UserMixin

db = SQLAlchemy()
login_manager = LoginManager()


class Recruiter(db.Model, UserMixin):
    
    __tablename__ = 'Recruiter'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    full_name = db.Column(db.String(300))
    password = db.Column(db.String(200))
    created_at = db.Column(db.String(200))
    company_name = db.Column(db.String(200))
    job_posted = db.Column(db.Boolean, unique=False)
    contact_number = db.Column(db.String(15))


    def __init__(self, email, full_name, password, created_at, company_name, job_posted, contact_number):
        self.full_name = full_name
        self.email = email
        self.password = password
        self.created_at = created_at
        self.company_name = company_name
        self.job_posted = job_posted
        self.contact_number = contact_number


class Student(db.Model, UserMixin):
    
    __tablename__ = 'Student'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    full_name = db.Column(db.String(300))
    password = db.Column(db.String(200))
    created_at = db.Column(db.String(200))
    department = db.Column(db.String(200))
    applied_to_job = db.Column(db.Boolean, unique=False)
    contact_number = db.Column(db.String(15))


    def __init__(self, email, full_name, password, created_at, department, applied_to_job, contact_number):
        self.full_name = full_name
        self.email = email
        self.password = password
        self.created_at = created_at
        self.department = department
        self.applied_to_job = applied_to_job
        self.contact_number = contact_number



class CSO(db.Model, UserMixin):
    
    __tablename__ = 'CSO'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    full_name = db.Column(db.String(300))
    password = db.Column(db.String(200))
    created_at = db.Column(db.String(200))
    campus_name = db.Column(db.String(200))


    def __init__(self, email, full_name, password, created_at, campus_name):
        self.full_name = full_name
        self.email = email
        self.password = password
        self.created_at = created_at
        self.campus_name = campus_name

@login_manager.user_loader
def user_loader(email):
    user = Recruiter.query.filter_by(email=email).one_or_none()
    if not user:
        return None
    else:
        return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    user = Recruiter.query.filter_by(email=email).one_or_none()
    return user if user else None
