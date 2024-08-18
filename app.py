from flask import Flask, render_template, request
from Flask_links import locations

app = Flask(__name__)

@app.route("/")
def Home():
    return render_template("Home.html")

@app.route("/Register")
def Teacher_Register():
    return render_template("ForTeacherRegistration.html")

@app.route("/Login")
def Teacher_login():
    return render_template("ForTeachersLogin.html")

@app.route("/StudentRegister")
def Student_Register():
    return render_template("ForStudentRegistration.html")

@app.route("/StudentLogin")
def Student_Login():
    return render_template("ForStudentLogin.html")






















locations(app)

if __name__ == "__main__":
    app.run(debug = True)