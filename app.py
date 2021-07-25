# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from security import Hash
from sqlalchemy import Column, Integer, String, Boolean
from forms import LoginForm, CreateRecruiterForm
from werkzeug.utils import secure_filename
import datetime, time
import csv
from csv import reader
from datetime import datetime,timedelta,date
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
import json
import io
import pandas as pd
import random, string
from flask_mail import Mail, Message

# Flask constructor takes the name of s
# current module (__name__) as argument.
app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'qira.ahmad@gmail.com'
app.config['MAIL_PASSWORD'] = 'datasstho123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

POSTGRES = {
    'user': 'postgres',
    'pw': '123456',
    'db': 'campus_career_portal',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

app.config['SECRET_KEY'] = 'ccp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db, Recruiter, CSO, Student, Users, login_manager, Job_Post, Employment_Type, User_Roles
from django.conf import settings

settings.configure()

db.init_app(app) 
login_manager.init_app(app) 
mail = Mail(app)


with app.app_context():
    db.create_all()
    db.session.commit()    # <- Here commit changes to database


# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/learn_more')
def learn_more():
    return render_template("learn_more.html")

@app.route('/calendar')
def calendar():
    return render_template("calendar.html")

@app.route('/cso_dashboard')
def cso_dashboard():
    return render_template("cso_dashboard.html")

@app.route('/student_dashboard')
def student_dashboard():
    return render_template("student_dashboard.html")

@app.route('/recruiter_dashboard')
def recruiter_dashboard():
    return render_template("recruiter_dashboard.html")
  
@app.route('/student_search_job')
def search_job_student_dashboard():
    posts = db.session.query(Job_Post).filter_by(status=True).all()
    e_type = []
    c_info = []
    for job in posts:
        employment_type = db.session.query(Employment_Type).filter_by(employment_type_id=job.employment_type).first()
        e_type.append(employment_type.description)
        company = db.session.query(Recruiter).filter_by(user_id=job.user_id).first()
        c_info.append(company.company_name)

    return render_template("search_job_student.html", posts=zip(posts, e_type, c_info))

@app.route('/view_students_jobs')
def view_student_jobs():
    return render_template("view_student_jobs.html")

@app.route('/view_all_jobs')
def view_all_jobs():
    posts = db.session.query(Job_Post).filter_by(user_id=session["user_id"]).all()
    e_type = []
    c_info = []
    for job in posts:
        employment_type = db.session.query(Employment_Type).filter_by(employment_type_id=job.employment_type).first()
        e_type.append(employment_type.description)
        company = db.session.query(Recruiter).filter_by(user_id=session["user_id"]).first()
        c_info.append(company.company_name)

    return render_template("view_recruiter_jobs.html", posts=zip(posts, e_type, c_info))

@app.route('/view_submitted_jobs')
def view_submitted_jobs():
    posts = db.session.query(Job_Post).filter_by(status=False).all()
    e_type = []
    c_info = []
    for job in posts:
        employment_type = db.session.query(Employment_Type).filter_by(employment_type_id=job.employment_type).first()
        e_type.append(employment_type.description)
        company = db.session.query(Recruiter).filter_by(user_id=job.user_id).first()
        c_info.append(company.company_name)

    return render_template("view_cso_jobs.html", posts=zip(posts, e_type, c_info))

@app.route('/view_students')
def view_students():
    students = db.session.query(Users).all()
    info = []
    for user in students:
        student_info = db.session.query(Student).filter_by(user_id=user.id).first()
        if student_info is not None:
            info.append(student_info)

    return render_template("view_students.html", posts=zip(students, info))

@app.route('/view_recruiters')
def view_recruiters():
    students = db.session.query(Users).all()
    info = []
    for user in students:
        student_info = db.session.query(Recruiter).filter_by(user_id=user.id).first()
        if student_info is not None:
            info.append(student_info)

    return render_template("view_recruiters.html", posts=zip(students, info))

@app.route('/view_active_jobs')
def view_active_jobs():
    posts = db.session.query(Job_Post).all()
    e_type = []
    c_info = []
    for job in posts:
        employment_type = db.session.query(Employment_Type).filter_by(employment_type_id=job.employment_type).first()
        e_type.append(employment_type.description)
        company = db.session.query(Recruiter).filter_by(user_id=session["user_id"]).first()
        c_info.append(company.company_name)

    return render_template("view_recruiter_jobs.html", posts=zip(posts, e_type, c_info))

@app.route('/view-job-details-student')
def view_job_details_dashboard():
    return render_template("view-job-details-student.html")

@app.route('/apply_now_form_student')
def apply_now_form_student():
    return render_template("apply_now_form_student.html")

@app.route('/approve_posting')
def approve_posting():
    return render_template("approve_posting.html")

@app.route('/job_approval_response')
def job_approval_response():
    return render_template("job_approval_response.html")

@app.route('/search_students')
def employer_search_students_response():
    return render_template("search_students_filter.html")
    #return render_template("employer_search_students.html")

@app.route('/apply_student_filter')
def search_students_filter():
    return render_template("search_students_filter.html")

@app.route('/upload_data_CSO')
def upload_data_CSO():
    return render_template("upload_data_CSO.html")

@app.route('/upload_doc', methods = ['GET', 'POST'])
def upload_doc():
    if request.method == 'POST':
          f = request.files['file']
          #filename = secure_filename(f.filename)  
          filestream = f.read()
          df = pd.read_csv(io.BytesIO(bytearray(filestream)))
          data_columns = list(df.columns.values.tolist())
          name, batch, roll_no, dept, email, contact_no = '', '', '', '', '', ''
          password = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))

          for index, row in df.iterrows():
            for c in data_columns:
              if 'name' in c or 'Name' in c:
                name = row[c]
              if 'batch' in c or 'Batch' in c:
                batch = row[c]
              if 'Roll' in c or 'roll' in c:
                roll_no = row[c]
              if 'email' in c or 'Email' in c:
                email = row[c]    
              if 'dept' in c or 'department' in c or 'Department' in c:
                dept = row[c]   
              if 'contact' in c or 'Contact' in c or 'phone' in c or 'Phone' in c:
                contact_no = row[c]  

            user = Users(
                    email = email, full_name=name,
                    password = Hash.hash_password(password),
                    contact_number = contact_no, role_id=2,
                    created_at = str(datetime.now()).split('.')[0])   
            db.session.add(user)
            db.session.commit()


            student = Student(
            user_id = user.id,
            department = dept, applied_to_job=False,
            created_at = str(datetime.now()).split('.')[0])
            db.session.add(student)
            db.session.commit()

            msg = Message('Welcome to Campus Career Portal!', sender = 'qira.ahmad@gmail.com', recipients = [email])
            msg.body = f' Hi { user.full_name }, Welcome to Campus Career Portal! Following are your account details: Email: {user.email} Password: {password}.'
            mail.send(msg)

    return render_template("upload_data_CSO.html", msg="Users have been registered")

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():    
    if request.method == 'POST':
        skills = []
        data = request.get_json()
        
        for i in data['skills']:
            if i=='':
                del i
            else:
                skills.append(i)

        skills = json.dumps(skills)

        if (data['job_type'] == 'Full-time'):
            job_post = Job_Post(
                        user_id = session['user_id'], location=data['city'],
                        job_title = data['job'], employment_type = 1,
                        skills = skills, job_description=data['jd'], status=False,
                        created_at = str(datetime.now()).split('.')[0])
            db.session.add(job_post)
            db.session.commit()
        elif (data['job_type'] == 'Part-time'):
            job_post = Job_Post(
                        user_id = session['user_id'], location=data['city'],
                        job_title = data['job'], employment_type = 2,
                        skills = skills, job_description=data['jd'], status=False,
                        created_at = str(datetime.now()).split('.')[0])
            db.session.add(job_post)
            db.session.commit()
        elif (data['job_type'] == 'Contract'):
            job_post = Job_Post(
                        user_id = session['user_id'], location=data['city'],
                        job_title = data['job'], employment_type = 3,
                        skills = skills, job_description=data['jd'], status=False,
                        created_at = str(datetime.now()).split('.')[0])
            db.session.add(job_post)
            db.session.commit()
        else:
            job_post = Job_Post(
                        user_id = session['user_id'], location=data['city'],
                        job_title = data['job'], employment_type = 4,
                        skills = skills, job_description=data['jd'], status=False,
                        created_at = str(datetime.now()).split('.')[0])
            db.session.add(job_post)
            db.session.commit()


        return render_template("post_job.html")

    else:
        return render_template("post_job.html")


@app.route('/view_uploaded_students_CSO')
def view_uploaded_students_CSO():
    return render_template("view_uploaded_students_CSO.html")

@app.route('/apply_job_final')
def final_job_apply():
    return render_template("apply_now_form_student_1.html")

@app.route('/create_recruiter', methods=['GET', 'POST'])
def create_recruiter():
    create_account_form = CreateRecruiterForm(request.form)
    login_form = LoginForm()
    if request.method == 'POST':
        full_name = request.form['full_name']
        email     = request.form['email']
        contact = request.form['contact_number']
        company = request.form['company_name']
        pw     = request.form['password']
        c_pw     = request.form['password_confirm']

        if pw!=c_pw:
            return render_template( 'sign_in.html', msg='Passwords do not match', form=create_account_form, form1=login_form)

        user=db.session.query(Users).filter_by(email=email).first()
        if user:
            return render_template( 'sign_in.html', msg='Email already registered', form=create_account_form, form1=login_form)

        # else we can create the user
        user = Users(
                    email = request.form['email'], full_name=full_name,
                    password = Hash.hash_password(request.form['password']),
                    contact_number = contact, role_id=1,
                    created_at = str(datetime.now()).split('.')[0])
        db.session.add(user)
        db.session.commit()

                # else we can create the user
        recruiter = Recruiter(
                    user_id = user.id,
                    company_name = company, job_posted=False,
                    created_at = str(datetime.now()).split('.')[0])
        db.session.add(recruiter)
        db.session.commit()

        return render_template('sign_in.html', msg='User created please <a href="/login">login</a>', form=create_account_form, 
        form1=login_form)

    else:
        return render_template('sign_in.html', form=create_account_form, form1=login_form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    register_form = CreateRecruiterForm()
    if request.method == 'POST':
        # read form data
        email = request.form['email']
        password = request.form['password']
        user=db.session.query(Users).filter_by(email=email).first()

        if user is None:
            return render_template('sign_in.html', msg="Invalid credentials, try again", form1=login_form, form=register_form)
        elif Hash.verify_password(user.password, password):
            login_user(user)
            session['username'] = email
            session['user_id'] = user.id

            if user.role_id == 1:
                return redirect(url_for('recruiter_dashboard'))
            elif user.role_id == 3:
                return redirect(url_for('cso_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:    
            return render_template('sign_in.html', msg="Invalid password, try again", form1=login_form, form=register_form)

    else:
        return render_template( 'sign_in.html', form1=login_form, form=register_form)

@app.route('/logout')
def logout():
    logout_user()
    session['user_id']=False
    session.pop('username', None)
    return redirect(url_for('login'))
    

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)
