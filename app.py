from flask import Flask, render_template, request
from Flask_links import locations

app = Flask(__name__)

def Direct_links(app):

    @app.route("/")
    def Home(): 
        return render_template("Home.html") # Home page

    @app.route("/Register")
    def Teacher_Register():
        return render_template("ForTeacherRegistration.html") # Teacher Registration page

    @app.route("/Login")
    def Teacher_login(): 
        return render_template("ForTeachersLogin.html") # Teacher Log In Page

    @app.route("/StudentRegister")
    def Student_Register():
        return render_template("ForStudentRegistration.html") #Student Registration page

    @app.route("/StudentLogin")
    def Student_Login():
        return render_template("ForStudentLogin.html") # Student Log In Page



if __name__ == "__main__":
    app.run(debug = True)