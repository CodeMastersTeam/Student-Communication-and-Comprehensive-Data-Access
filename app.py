from flask import Flask, render_template, request, session, redirect, url_for
from Flask_links import locations
from Database import *
app = Flask(__name__)


def Direct_links(app):

    @app.route("/")
    def Home(): 
        return render_template("Home.html") # Home page

    @app.route("/Register")
    def Teacher_Register():
        return render_template("ForTeacherRegistration.html") # Teacher Registration page

    @app.route("/StudentsRegister")
    def Student_Register():
        return render_template("ForStudentRegistration.html") #Student Registration page

    @app.route("/StudentsLogin")
    def Student_Login():
        return render_template("ForStudentLogin.html") # Student Log In Page
    
    @app.route("/Login")
    def Teacher_login(): 
        return render_template("ForTeachersLogin.html") # Teacher Log In Page

    
    @app.route('/logout') # Log out
    def Student_logout():
        session.pop('username',None)
        return redirect(url_for("Home"))

   
    @app.route("/Student_Home") # Student Home page
    def Student_Home():
        username = session['username']
        return render_template("Student_Home_Page.html", username = username)
    
    @app.route("/Teacher_Home") # Student Home page
    def Teacher_Home():
        username = session['username']
        return render_template("Teacher_Home_Page.html", username = username)
    
    