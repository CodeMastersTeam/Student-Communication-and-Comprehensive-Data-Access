from flask import Flask, request, render_template, flash, redirect, url_for, session
from Registration import *

app = Flask(__name__)

# class Locations:
#     def __init__(self, x):
#         self.x = x
# 
#     def ruotes(self):
#         return app.route(self.x)
# 
# 
# x = Locations("/")
# @x.ruotes()
# def Home():
#     return render_template("Teachers.html")

def locations(app):

    @app.route("/Registration_links", methods = ["POST", "GET"])
    def Registration():
        link = request.form.get("link")
        if request.method == "POST":
            if link == "Teacher":
                return render_template("Teachers.html")
            elif link == "Student":
                return render_template("Students.html")
        else:
            return render_template("Home.html")


    @app.route("/Inputs", methods = ["GET", "POST"])
    def StudentRegistration():
        if request.method == "POST":
            firstname = str(request.form["firstname"])
            middlename = str(request.form["middlename"])
            lastname = str(request.form["lastname"])
            age = request.form["age"]
            address = str(request.form["address"])
            sex = sex = request.form.get("sex")
            cellphone_number = str(request.form["cellphone_number"])
            Birth_date = str(request.form["Birth_date"])
            Birth_place = str(request.form["Birth_place"])
            Username = str(request.form["Student_Username"])
            Password = str(request.form["Student_Password"])
            Course = str(request.form["Course"])
            Year = str(request.form["Year"])


            ForStudentRegistration(
                firstname, middlename, lastname, age, address, sex, 
                cellphone_number, Birth_date, Birth_place, Username, Password, Course, Year
            )

            return render_template("ForStudentRegistration.html")

        else:
            return render_template("ForStudentRegistration.html")
        
    
    @app.route("/TeacherInputs", methods = ["GET", "POST"])
    def TeacherRegistration():
        if request.method == "POST":
            firstname = str(request.form["firstname"])
            middlename = str(request.form["middlename"])
            lastname = str(request.form["lastname"])
            age = request.form["age"]
            address = str(request.form["address"])
            sex = sex = request.form.get("sex")
            cellphone_number = str(request.form["cellphone_number"])
            Birth_date = str(request.form["Birth_date"])
            Birth_place = str(request.form["Birth_place"])
            Username = str(request.form["Teacher_Username"])
            Password = str(request.form["Teacher_Password"])
            Course = str(request.form["Course"])
            Year = str(request.form["Year"])


            ForTeacherRegistration(
                firstname, middlename, lastname, age, address, sex, 
                cellphone_number, Birth_date, Birth_place, Username, Password, Course, Year
            )

            return render_template("ForTeacherRegistration.html")

        else:
            return render_template("ForTeacherRegistration.html")

    @app.route("/StudentsLogin", methods = ["POST"])
    def Students_Login():
        username = request.form["LoginUsername"]
        password = request.form["LoginPassword"]
        db.execute("SELECT * FROM student_informations WHERE username = %s AND Password = %s", (username, password))
        user = db.fetchone()
        #db.close()
        
        if user:
            session["Student"] = username
            return render_template("Profile.html")
        else:
            flash("Incorrect credentials")
            return redirect(url_for("Students_Login"))
        
        return render_template("ForStudentLogin.html")
    
    @app.route("/TeacherLogin", methods=["POST"])
    def Teachers_Login():
        username = request.form.get("LoginUsername")
        password = request.form.get("LoginPassword")

        if username and password:
            db.execute("SELECT * FROM teacher_informations WHERE username = %s AND Password = %s", (username, password))
            user = db.fetchone()
            if user:
                session["Teacher"] = username
                return render_template("Profile.html")
            else:
                flash("Log in failed!")
                return redirect(url_for("Teacher_login"))
        else:
            flash("Missing username or password!")
            return redirect(url_for("Teacher_login"))

    





if __name__ == "__main__":

    app.run(debug = True)