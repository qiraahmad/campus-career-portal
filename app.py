# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template
  
# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
  
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
def index():
    return render_template("sign_in.html")

@app.route('/learn_more')
def learn_more():
    return render_template("learn_more.html")

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
    return render_template("search_job_student.html")


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
    return render_template("employer_search_students.html")

<<<<<<< HEAD
@app.route('/apply_student_filter')
def search_students_filter():
    return render_template("search_students_filter.html")
=======
@app.route('/upload_data_CSO')
def upload_data_CSO():
    return render_template("upload_data_CSO.html")


@app.route('/view_uploaded_students_CSO')
def view_uploaded_students_CSO():
    return render_template("view_uploaded_students_CSO.html")
>>>>>>> 6ad92ca0b3df6787d3ad1d4df004bbcdb5ab6962


# main driver function
if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.

    #coo
    app.run()