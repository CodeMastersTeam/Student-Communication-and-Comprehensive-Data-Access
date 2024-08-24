from flask import Flask, request, render_template, flash, redirect, url_for, session
from Database import *
import os


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
            Password1 = str(request.form["Student_Password1"])
            Password2 = str(request.form["Student_Password2"])
            Course = str(request.form["Course"])
            Year = str(request.form["Year"])

            db.execute("SELECT * FROM student_informations WHERE username = %s", (Username,))
            existing_user = db.fetchone()
            if existing_user:
                flash("Username already taken, please choose another one!", "error")
                return render_template("ForStudentRegistration.html")

            if Password1 != Password2:
                flash("Password should be a same!", "error")
                return render_template("ForStudentRegistration.html")

            if len(Password1) < 8:
                flash("Password should be more than 8 characters!", "error")
                return render_template("ForStudentRegistration.html")
            
        
            ForStudentRegistration(
                firstname, middlename, lastname, age, address, sex, 
                cellphone_number, Birth_date, Birth_place, Username, Password1, Course, Year
            )
            flash("Registered successfully!", "success")
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
            Password1 = str(request.form["Teacher_Password1"])
            Password2 = str(request.form["Teacher_Password2"])
            Course = str(request.form["Course"])
            Year = str(request.form["Year"])

            db.execute("SELECT * FROM teacher_informations WHERE username = %s", (Username,))
            existing = db.fetchone()
            if existing:
                flash("Username already taken, please choose another one!", "error")
                return render_template("ForTeacherRegistration.html")

            
            if Password1 != Password2:
                flash("Password should be a same!", "error")
                return render_template("ForTeacherRegistration.html")

            if len(Password1) < 8:
                flash("Password should be more than 8 characters!", "error")
                return render_template("ForTeacherRegistration.html")

            else:
                ForTeacherRegistration(
                firstname, middlename, lastname, age, address, sex, 
                cellphone_number, Birth_date, Birth_place, Username, Password1, Course, Year
                )
                flash("Registered successfully!", "success")
                
            
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
            session["username"] = username
            return redirect(url_for("Student_Home"))
        else:
            flash("Invalid username or password!", "error")
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
                session["username"] = username
                return redirect(url_for("Teacher_Home"))
            else:
                flash("Invalid username or password!", "error")
                return redirect(url_for("Teacher_login"))
        else:
            flash("Missing username or password!")
            return redirect(url_for("Teacher_login"))
    
    
    
    @app.route("/updatepass",methods=["POST","GET"])
    def updatepass():
        if request.method == "POST":
            username = session['username']
            password1 = request.form['updatepassword1']
            password2 = request.form['updatepassword2']
            if password1 != password2:
                flash("Password should be the same!", "error")
                return render_template("update.html")
            
            if len(password1) < 8:
                flash("Password should be more than 8 characters!", "error")
                return render_template("update.html")
            

            else:
                db.execute("UPDATE student_informations SET password = %s WHERE username = %s",(password1,username))
                Connect.commit()
                flash("Updated sucessfuly!", "success")
        return render_template("update.html")
    

    







if __name__ == "__main__":
    app.run(debug = True)