# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
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
import psycopg2
import numpy as np
import ast

# Flask constructor takes the name of s
# current module (__name__) as argument.
app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'campuscareerportal@gmail.com'
app.config['MAIL_PASSWORD'] = '123awesome'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

conn = psycopg2.connect(
   database="campus_career_portal", user='postgres', password='123', host='127.0.0.1', port= '5432'
)
cursor = conn.cursor()

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

from models import *
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

@app.route('/view_feedback/<job_id>', methods = ['GET', 'POST'])
def view_feedback(job_id):
    job = db.session.query(Job_Post).filter_by(id=job_id).first()
    employment_type = db.session.query(Employment_Type).filter_by(employment_type_id=job.employment_type).first()
    company = db.session.query(Recruiter).filter_by(user_id=job.user_id).first()
    return render_template("view_feedback.html", data=job, employment_type=employment_type, company=company)

@app.route('/view_applicants/<job_id>', methods = ['GET', 'POST'])
def view_applicants(job_id):
    job_apps = db.session.query(Job_Application).filter_by(job_id=job_id).all()
    info = []
    students = []
    for j in job_apps:
        student_info = db.session.query(Student).filter_by(user_id=j.user_id).first()
        if student_info is not None:
            info.append(student_info)
        students.append(db.session.query(Users).filter_by(id=j.user_id).first())

    return render_template("view_applicants.html", posts=zip(students, info), j_id=job_id)
  
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
    posts = db.session.query(Job_Post).filter_by(status=True).all()
    e_type = []
    c_info = []
    for job in posts:
        employment_type = db.session.query(Employment_Type).filter_by(employment_type_id=job.employment_type).first()
        e_type.append(employment_type.description)
        company = db.session.query(Recruiter).filter_by(user_id=job.user_id).first()
        c_info.append(company.company_name)

    return render_template("view_student_jobs.html", posts=zip(posts, e_type, c_info))

@app.route('/view_applied_jobs')
def view_applied_jobs():
    posts = db.session.query(Job_Application).filter_by(user_id=session["user_id"]).all()
    jobs = []
    e_type = []
    c_info = []
    status = []
    for app in posts:
        job = db.session.query(Job_Post).filter_by(id=app.job_id).first()
        jobs.append(job)
        employment_type = db.session.query(Employment_Type).filter_by(employment_type_id=job.employment_type).first()
        e_type.append(employment_type.description)
        company = db.session.query(Recruiter).filter_by(user_id=job.user_id).first()
        c_info.append(company.company_name)
        status.append(app.status)

    return render_template("view_applied_jobs.html", posts=zip(jobs, e_type, c_info, status))

@app.route('/view_student_applications')
def view_student_applications():
    posts = db.session.query(Job_Application).all()
    jobs = []
    e_type = []
    status = []
    user = []
    student = []
    for app in posts:
        job = db.session.query(Job_Post).filter_by(id=app.job_id).first()
        jobs.append(job)
        employment_type = db.session.query(Employment_Type).filter_by(employment_type_id=job.employment_type).first()
        e_type.append(employment_type.description)
        status.append(app.status)
        u = db.session.query(Users).filter_by(id=app.user_id).first()
        s = db.session.query(Student).filter_by(user_id=app.user_id).first()
        user.append(u)
        student.append(s)

    return render_template("view_student_applications.html", posts=zip(jobs, e_type, status, user, student))

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
    posts = db.session.query(Job_Post).all()
    e_type = []
    c_info = []
    for job in posts:
        employment_type = db.session.query(Employment_Type).filter_by(employment_type_id=job.employment_type).first()
        e_type.append(employment_type.description)
        company = db.session.query(Recruiter).filter_by(user_id=job.user_id).first()
        c_info.append(company.company_name)

    return render_template("view_cso_jobs.html", posts=zip(posts, e_type, c_info))

@app.route('/view_job/<job_id>', methods = ['GET', 'POST'])
def view_job(job_id):
    job = db.session.query(Job_Post).filter_by(id=job_id).first()
    employment_type = db.session.query(Employment_Type).filter_by(employment_type_id=job.employment_type).first()
    company = db.session.query(Recruiter).filter_by(user_id=job.user_id).first()
    return render_template("view_job.html", data=job, employment_type=employment_type, company=company)
    
@app.route('/apply_for_job/<job_id>', methods = ['GET', 'POST'])
def apply_for_job(job_id):
    job = db.session.query(Job_Post).filter_by(id=job_id).first()
    employment_type = db.session.query(Employment_Type).filter_by(employment_type_id=job.employment_type).first()
    company = db.session.query(Recruiter).filter_by(user_id=job.user_id).first()
    return render_template("apply_for_job.html", data=job, employment_type=employment_type, company=company)

@app.route('/submit_application/<job_id>', methods = ['GET', 'POST'])
def submit_application(job_id):
    app = Job_Application(
            user_id = session["user_id"], job_id=job_id, status="Application Submitted",
            created_at = str(datetime.now()).split('.')[0])   

    db.session.add(app)
    db.session.commit()

    return render_template("job_post_status.html", status_msg="Job Application Submitted!")    

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
    posts = db.session.query(Job_Post).filter_by(status=True).all()
    e_type = []
    c_info = []
    for job in posts:
        employment_type = db.session.query(Employment_Type).filter_by(employment_type_id=job.employment_type).first()
        e_type.append(employment_type.description)
        company = db.session.query(Recruiter).filter_by(user_id=session["user_id"]).first()
        c_info.append(company.company_name)

    return render_template("view_active_jobs.html", posts=zip(posts, e_type, c_info))

@app.route('/view_approved_jobs')
def view_approved_jobs():
    posts = db.session.query(Job_Post).filter_by(status=True).all()
    e_type = []
    c_info = []
    for job in posts:
        employment_type = db.session.query(Employment_Type).filter_by(employment_type_id=job.employment_type).first()
        e_type.append(employment_type.description)
        company = db.session.query(Recruiter).filter_by(user_id=job.user_id).first()
        c_info.append(company.company_name)

    return render_template("view_approved_jobs.html", posts=zip(posts, e_type, c_info))


@app.route('/update_job/<job_id>', methods = ['GET', 'POST'])
def update_job_status(job_id):
    feedback = request.form.get('text')
    data = request.form['status']
    job = db.session.query(Job_Post).filter_by(id=job_id).first()
    status_msg = ''
    if data == 'Approve':
        job.status = True;
        job.message = feedback
        status_msg = "Job approved!"
    else:
        job.status = False
        job.message = feedback
        status_msg = "Job rejected!"

    db.session.commit()
    return render_template("job_post_status.html", status_msg=status_msg)

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
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = '''
        SELECT 
            s."student_id" as user_id, u."full_name", s."department", concat('20', substring(u."email" from 2 for 2)) as batch
        FROM public."Student" s
        join public."Users" u on u.id = s.user_id '''
    cur.execute(s) # Execute the SQL    
    list_users = cur.fetchall()
    cur.close
    return render_template("search_students_filter.html", students=list_users)
    #return render_template("employer_search_students.html")

@app.route('/view_student/<student_id>', methods = ['GET', 'POST'])
def view_student(student_id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = '''
        SELECT 
            s."student_id" as user_id, u."full_name", s."department", concat('20', substring(u."email" from 2 for 2)) as batch
        FROM public."Student" s
        join public."Users" u on u.id = s.user_id
        where s."student_id" = {} '''.format(student_id)
    cur.execute(s) # Execute the SQL    
    student = cur.fetchall()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = '''
        SELECT 
			c."Course_Title",
			g.grade
        FROM public."Student_Courses" sc
        join public."Users" u on u.id = sc.user_id
		join public."Student" s on s.user_id = sc.user_id
		join public."Course_Catalog" c on c.id = sc.course_id
		join public."Grades" g on g.id = sc.grade_id
        where s."student_id" = {} '''.format(student_id)
    cur.execute(s) # Execute the SQL   
    course_info = cur.fetchall()
    return render_template("view_student.html", data=student, course_info=course_info)

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

            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            s = '''
               INSERT INTO public."Users"(
	        email, role_id, full_name, password, created_at, contact_number)
	        VALUES ('{}', 2, '{}', '{}', '{}', '{}') RETURNING id'''.format(email, name, Hash.hash_password(password), str(datetime.now()).split('.')[0], contact_no)
            cur.execute(s) # Execute the SQL 
            conn.commit()
            user_id = cur.fetchall()
            cur.close()

            student = Student(
            user_id = user_id[0][0],
            department = dept, applied_to_job=False,
            created_at = str(datetime.now()).split('.')[0])
            db.session.add(student)
            db.session.commit()

            msg = Message('Welcome to Campus Career Portal!', sender = 'qira.ahmad@gmail.com', recipients = [email])
            msg.body = f' Hi { name }, Welcome to Campus Career Portal! Following are your account details: Email: {email} Password: {password}.'
            mail.send(msg)
            print("Password", password)

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
                        created_at = str(datetime.now()).split('.')[0], message=None)
            db.session.add(job_post)
            db.session.commit()
        elif (data['job_type'] == 'Part-time'):
            job_post = Job_Post(
                        user_id = session['user_id'], location=data['city'],
                        job_title = data['job'], employment_type = 2,
                        skills = skills, job_description=data['jd'], status=False,
                        created_at = str(datetime.now()).split('.')[0], message=None)
            db.session.add(job_post)
            db.session.commit()
        elif (data['job_type'] == 'Contract'):
            job_post = Job_Post(
                        user_id = session['user_id'], location=data['city'],
                        job_title = data['job'], employment_type = 3,
                        skills = skills, job_description=data['jd'], status=False,
                        created_at = str(datetime.now()).split('.')[0], message=None)
            db.session.add(job_post)
            db.session.commit()
        else:
            job_post = Job_Post(
                        user_id = session['user_id'], location=data['city'],
                        job_title = data['job'], employment_type = 4,
                        skills = skills, job_description=data['jd'], status=False,
                        created_at = str(datetime.now()).split('.')[0], message=None)
            db.session.add(job_post)
            db.session.commit()


        return render_template("post_job.html")

    else:
        skills = db.session.query(Skills).all()
        return render_template("post_job.html", skills=skills)

@app.route("/livesearch",methods=["POST","GET"])
def livesearch():
    searchbox = request.form.get("text")
    query = '''select name from public."Skills" where name ILIKE '%{}%' '''.format(searchbox)
    cursor.execute(query)
    result = cursor.fetchall()
    return jsonify(result)

@app.route("/course_catalog",methods=["POST","GET"])
def course_catalog():
    searchbox = request.form.get("text")
    query = '''select "Course_Title" from public."Course_Catalog" where "Course_Title" ILIKE '%{}%' '''.format(searchbox)
    cursor.execute(query)
    result = cursor.fetchall()
    return jsonify(result)

@app.route("/add_courses",methods=["POST","GET"])
def add_courses():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = ('''
        SELECT 
            sc.id, u.full_name, cc."Course_Title", g.grade, date(sc.created_at) as created_at
        FROM public."Student_Courses" sc
        join public."Users" u on u.id = sc.user_id
        join public."Course_Catalog" cc on cc.id = sc.course_id
        join public."Grades" g on g.id = sc.grade_id
        where sc.user_id = {0} '''.format(session["user_id"]))
    cur.execute(s) # Execute the SQL    
    list_users = cur.fetchall()
    query = '''select "Course_Title" as name from public."Course_Catalog" '''
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query)
    courses = cur.fetchall()
    query = '''select "grade" as name from public."Grades" '''
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query)
    grades = cur.fetchall()
    return render_template('add_courses.html', list_users = list_users, courses=courses, grades=grades, first_time_login=session['first_time_login'])


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
            if user.first_time_login == False:
                session['first_time_login'] = True
                user.first_time_login = True
            else:
                session['first_time_login'] = False
                user.first_time_login = False

            session['user_id'] = user.id
            user.last_login_at = datetime.now()
            db.session.commit()


            if user.role_id == 1:
                return redirect(url_for('recruiter_dashboard'))
            elif user.role_id == 3:
                return redirect(url_for('cso_dashboard'))
            elif user.role_id == 2:
                data = db.session.query(Student_Courses).filter_by(user_id=user.id).all()
                if len(data) >= 5:
                    return redirect(url_for('student_dashboard'))
                else:
                    return redirect(url_for('add_courses'))
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
 
@app.route('/add_student_course', methods=['POST'])
def add_student_course():
    if request.method == 'POST':
        course = request.form.get('course_select')
        grade = request.form.get('grade_select')
        grade = db.session.query(Grades).filter_by(grade=grade).first()
        course = db.session.query(Course_Catalog).filter_by(Course_Title=course).first()
        student_course = db.session.query(Student_Courses).filter_by(course_id=course.id, user_id=session["user_id"]).first()

        if not student_course:
            sc = Student_Courses(
                user_id = session["user_id"], course_id=course.id, grade_id=grade.id,
                created_at = datetime.now())   

            db.session.add(sc)
            db.session.commit()
            flash('Student Added successfully')
        else:
            flash('Course Data Against Student Exists')

        return redirect(url_for('add_courses'))
 
@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_student_course(id):   
    data = db.session.query(Student_Courses).filter_by(id=id).first()
    query = '''select "grade" as name from public."Grades" '''
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query)
    courses = cur.fetchall()
    cur.close()

    course = db.session.query(Course_Catalog).filter_by(id=data.id).first()
    return render_template('edit.html', student = data, courses = courses, update_course=course.Course_Title)
 
@app.route('/update/<id>', methods=['POST'])
def update_student_course(id):
    if request.method == 'POST':
        grade = request.form.get('grade_select')
        grade = db.session.query(Grades).filter_by(grade=grade).first()

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE public."Student_Courses"
            SET grade_id = %s
            WHERE id = %s
        """, (grade.id, id))
        flash('Student Updated Successfully')
        conn.commit()
        return redirect(url_for('add_courses'))
 
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_student(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('DELETE FROM public."Student_Courses" WHERE id = {0}'.format(id))
    conn.commit()
    flash('Student Course Removed Successfully')
    return redirect(url_for('add_courses'))

def map_courses(user_id):
    # convert to lowercase
    query_string = ('''	SELECT lower(CONCAT(cc."Course_Title", ' ', cc."Course_Details")) as course
	FROM public."Student_Courses" sc
	join public."Grades" g on g.id = sc.grade_id
	join Public."Course_Catalog" cc on sc.course_id = cc.id
    WHERE sc.user_id = {0}'''.format(user_id))

    #Retrieving data
    cursor.execute(query_string)
    #Fetching 1st row from the table
    result = cursor.fetchall();
    res = list(map(' '.join, result))
    textsample = ' '.join([str(elem) for elem in res])

    query_string = '''SELECT name from public."Skills" where '{}' like CONCAT('%',lower(name),'%') '''.format(textsample)
    
    #Retrieving data
    cursor.execute(query_string)
    #Fetching 1st row from the table
    result = cursor.fetchall();
    res = [''.join(i) for i in result]
    return res


@app.route('/view_recommended_jobs')
def view_recommended_jobs():
    cs_mapping_curr_user = map_courses(session["user_id"])
    # print(cs_mapping_curr_user)
    skills = []
    jobs = []
    students = []

    query = '''	 select distinct user_id from public."Student"; '''
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query)
    st = cur.fetchall()
    for st1 in st:
            for st2 in st1:
                students.append(st2)

    query = '''	 select distinct id from public."Job_Post" where status = true; '''
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query)
    j = cur.fetchall()
    for j1 in j:
        for j2 in j1:
            jobs.append(j2)

    # print(skills, students, jobs)
    posts = db.session.query(Job_Post).filter_by(status=True).all()
    for p in posts:
        s = json.loads(p.skills)
        for i in s:
            skills.append(i)

    student_dict = {}
    scores = []
    for s_id in students:
        for j in skills:
            cs_mapping = map_courses(s_id)
            if j in cs_mapping:
                scores.append(1)
            else:
                scores.append(0)
        student_dict[s_id] = scores 
        scores = []


    # Create DataFrame  
    df = pd.DataFrame(student_dict, index=None)
    df = df.T
    df.columns = skills  
    df['user_id'] = students
    # Print the output.  
    print(df)   

    #Build the user user similarity matrix based on thier skill vectors
    #initialise a user user matrix uptill user count
    sim=list()
    for i in range(max(students)+1):
            l=list()
            l=[0]*(max(students)+1)
            sim.append(l)

    #Build  a dictionary of respondent id's as keys  and thier skills as values
    m=(np.asscalar(np.int32(max(students))))
    temp=[0]*m
    vector=np.array(temp)
    d=dict()
    df = df[ ['user_id'] + [ col for col in df.columns if col != 'user_id' ] ]
    for row in df.iterrows():
        index,data=row
        l=list()
        #l=[data.values[0],list(data.values[1:])]
        s=np.asscalar(np.int32(data.values[0]))
        d[s]=np.array(list(data.values[1:]))
        #print(type(data))

    for key, value in d.items():
            if(key< max(students)):
                b=(np.linalg.norm(value))
                for key2,value2 in d.items():
                    if(key2< max(students)):
                        # print(d[key],d[key2])
                        a=np.dot(d[key],d[key2])
                        ans=a/(np.linalg.norm(value2)*b)
                        sim[key][key2] = ans
                        #count2+=1
        #count1+=1
    rec_students = []
    jp = []
    for i in students:
        if session["user_id"] != i and max(sim[i]) > 0:
            rec_students.append(i)
            print(i, max(sim[i]), sim[i].index( max(sim[i])))
        # the similarity of user 1 with others 
        #print((max(sim[1][2:])))
        #print(sim[1].index(max(sim[1][2:])))
        #user 1 is most similar to user 4653 with similarity 0.71 in skills

    for i in rec_students:
        job_apps = db.session.query(Job_Application).filter_by(user_id=i).all()
        for j in job_apps:
            jp.append(db.session.query(Job_Post).filter_by(status=True, id=j.job_id).first())
    e_type = []
    c_info = []
    if jp:
        for job in jp:
            employment_type = db.session.query(Employment_Type).filter_by(employment_type_id=job.employment_type).first()
            e_type.append(employment_type.description)
            company = db.session.query(Recruiter).filter_by(user_id=job.user_id).first()
            c_info.append(company.company_name)
           

    return render_template("view_student_jobs.html", posts=zip(jp, e_type, c_info))



@app.route('/view_recommended_applicants/<job_id>', methods = ['POST', 'GET'])
def view_recommended_applicants(job_id):
    job_apps = db.session.query(Job_Application).filter_by(job_id=job_id).all()
    for j in job_apps:
        cs_mapping_curr_user = map_courses(j.user_id)
        # print(cs_mapping_curr_user)
        skills = []
        jobs = []
        students = []

        query = '''	 select distinct s.user_id from public."Student" s join public."Job_Application" ja on ja.user_id = s.user_id where ja.job_id = {}; '''.format(job_id)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query)
        st = cur.fetchall()
        for st1 in st:
                for st2 in st1:
                    students.append(st2)

        query = '''	 select distinct j.id from public."Job_Post" j join public."Job_Application" ja on ja.job_id = j.id where j.status = true and j.id = {}; '''.format(job_id)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query)
        j = cur.fetchall()
        for j1 in j:
            for j2 in j1:
                jobs.append(j2)

        # print(skills, students, jobs)
        posts = db.session.query(Job_Post).filter_by(status=True, id=job_id).all()
        for p in posts:
            s = json.loads(p.skills)
            for i in s:
                skills.append(i)

        student_dict = {}
        scores = []
        for s_id in students:
            for j in skills:
                cs_mapping = map_courses(s_id)
                if j in cs_mapping:
                    scores.append(1)
                else:
                    scores.append(0)
            student_dict[s_id] = scores 
            scores = []


        # Create DataFrame  
        df = pd.DataFrame(student_dict, index=None)
        df = df.T
        df['user_id'] = students
        df.columns = ['user_id'] + skills  

        job_skills = []
        skill_scores = []
        job_skill_dict = {}
        query = '''select skills #>> '{}' as skills, id from public."Job_Post" j where j.status = true '''
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query)
        j = cur.fetchall()
        for i in j:
            if int(i[1]) == int(job_id):
                l = ast.literal_eval(i[0])
                job_skills = [i.strip() for i in l]

        for j in skills:
            if j in job_skills:
                skill_scores.append(1)
            else:
                skill_scores.append(0)
        job_skill_dict[job_id] = skill_scores 

        # Create DataFrame  
        jdf = pd.DataFrame(job_skill_dict, index=None)
        jdf = jdf.T
        jdf['job_id'] = [job_id]
        jdf.columns = ['job_id'] + skills  

        info = []
        students = []
        score = []

        # iterating over rows using iterrows() function
        for i, j in jdf.loc[:, jdf.columns != 'job_id'].iterrows():
            job = np.asarray(j.astype(np.bool))
            for k, l in df.loc[:, df.columns != 'user_id'].iterrows():
                student = np.asarray(l.astype(np.bool))
                if job.shape != student.shape:
                    raise ValueError("Shape mismatch: im1 and im2 must have the same shape.")

                intersection = np.logical_and(job, student)

                union = np.logical_or(job, student)

                js = intersection.sum() / float(union.sum())

                student_info = db.session.query(Student).filter_by(user_id=k).first()
                if student_info is not None:
                    info.append(student_info)
                students.append(db.session.query(Users).filter_by(id=k).first())
                score.append(js)

        posts = sorted(zip(students, info, score), key = lambda x: x[2], reverse=True)
        return render_template("view_recommended.html", posts=posts)


    # main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)
