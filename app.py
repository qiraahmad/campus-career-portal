
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

# main driver function
if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()