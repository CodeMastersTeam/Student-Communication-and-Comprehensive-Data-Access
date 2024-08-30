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
            elif link == "Main":
                return render_template("Main.html")
        else:
            return render_template("Home.html")


    @app.route("/Inputs", methods=["GET", "POST"])
    def StudentRegistration():
        if request.method == "POST":
            firstname = str(request.form["firstname"])
            middlename = str(request.form["middlename"])
            lastname = str(request.form["lastname"])
            age = int(request.form["age"])  
            address = str(request.form["address"])
            sex = request.form.get("sex")
            cellphone_number = str(request.form["cellphone_number"])
            birth_date = str(request.form["Birth_date"])  
            birth_place = str(request.form["Birth_place"])
            username = str(request.form["Student_Username"])
            password1 = str(request.form["Student_Password1"])
            password2 = str(request.form["Student_Password2"])
            course = str(request.form["Course"])
            year = int(request.form["Year"]) 
            profile_picture = None  

            db.execute("SELECT * FROM students WHERE username = %s", (username,))
            existing_user = db.fetchone()
            if existing_user:
                flash("Username already taken, please choose another one!", "error")
                return render_template("ForStudentRegistration.html")

            if password1 != password2:
                flash("Passwords do not match!", "error")
                return render_template("ForStudentRegistration.html")

            if len(password1) < 8:
                flash("Password should be more than 8 characters!", "error")
                return render_template("ForStudentRegistration.html")

            db.execute("SELECT course_id FROM courses WHERE course_name = %s", (course,))
            course_data = db.fetchone()
            if not course_data:
                flash("Invalid course selected.", "error")
                return render_template("ForStudentRegistration.html")

            course_id = course_data[0]
            

            try:
                ForStudentRegistration_students(
                    firstname, middlename, lastname, age, address, sex, 
                    cellphone_number, birth_date, birth_place, username, 
                    password1, profile_picture, year, course_id
                )
                flash("Registered successfully!", "success")
            except Exception as e:
                flash(f"An error occurred: {e}", "error")

            return render_template("ForStudentRegistration.html")

        return render_template("ForStudentRegistration.html")

        
    
    @app.route("/TeacherInputs", methods = ["GET", "POST"])
    def TeacherRegistration():
        if request.method == "POST":
            firstname = str(request.form["firstname"])
            middlename = str(request.form["middlename"])
            lastname = str(request.form["lastname"])
            age = request.form["age"]
            address = str(request.form["address"])
            sex = request.form.get("sex")
            cellphone_number = str(request.form["cellphone_number"])
            Birth_date = str(request.form["Birth_date"])
            Birth_place = str(request.form["Birth_place"])
            Username = str(request.form.get("Teacher_Username"))
            Password1 = str(request.form.get("Teacher_Password1"))
            Password2 = str(request.form.get("Teacher_Password2"))
            Department = str(request.form["Department"])
            Year = str(request.form["Year"])
            Profile_Picture = None
            semester_id = None

            db.execute("SELECT * FROM teachers WHERE username = %s", (Username,))
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
                ForTeacherRegistration(firstname, middlename, lastname, age, address, sex, 
            cellphone_number, Birth_date, Birth_place, Username, Password1, Department, Profile_Picture, Year, semester_id)
                flash("Registered successfully!", "success")
                
            
            return render_template("ForTeacherRegistration.html")

        else:
            return render_template("ForTeacherRegistration.html")

    @app.route("/StudentsLogin", methods = ["POST"])
    def Students_Login():
        username = request.form["LoginUsername"]
        password = request.form["LoginPassword"]
        db.execute("SELECT * FROM students WHERE username = %s AND Password = %s", (username, password))
        user = db.fetchone()
        #db.close()
        
        if user:
            session["username"] = username
            return redirect(url_for("Student_Home"))
        else:
            flash("These credentials do not match our records.", "error")
            return redirect(url_for("Students_Login"))
            
        return render_template("ForStudentLogin.html")
    
    @app.route("/TeacherLogin", methods=["POST"])
    def Teachers_Login():
        username = request.form.get("LoginUsername")
        password = request.form.get("LoginPassword")

        if username and password:
            db.execute("SELECT * FROM teachers WHERE username = %s AND Password = %s", (username, password))
            user = db.fetchone()
            if user:
                session["username"] = username
                return redirect(url_for("Teacher_Home_Page"))
            else:
                flash("These credentials do not match our records.", "error")
                return redirect(url_for("Teacher_login"))
        else:
            flash("These credentials do not match our records.", "error")
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
                db.execute("UPDATE teachers SET password = %s WHERE username = %s",(password1,username))
                Connect.commit()
                flash("Updated sucessfulLy! Please log in again to continue.", "success")
        return render_template("update.html")
    
    
    @app.route("/Forgot_Pass")
    def Forgot_Pass():
        return render_template("Forgot_Pass.html")


    @app.route("/TeacherRecoverPass", methods = ["POST"])
    def TeacherRecoverPass():
        userrname = request.form["username"]
        db.execute(f"SELECT * FROM teachers WHERE username = '{userrname}'")
        user = db.fetchone()
        if user != None:
            session["username"] = userrname
            return redirect(url_for("updatepass"))
        else:
            flash("Email not found! Please create a new account instead", "error")
            return redirect(url_for("Forgot_Pass"))


    @app.route("/update_student_info", methods=["POST"])
    def update_student_info():
        if 'username' not in session:
            return redirect(url_for('Student_Login'))
    
        username = session['username']
        firstname = request.form.get('firstname')
        middlename = request.form.get('middlename')
        lastname = request.form.get('lastname')
        age = request.form.get('age')
        sex = request.form.get('sex')
        address = request.form.get('address')
        cellphone_number = request.form.get('cellphone_number')
        birth_date = request.form.get('Birth_date')
        birth_place = request.form.get('Birth_place')
        Username = request.form.get("username")
        password = request.form.get("password")
        profile_picture = None
    
        try:
            if not all([username, firstname, middlename, lastname, age, sex, address, cellphone_number, birth_date, birth_place, Username, password]):
                flash("Kompletoha tanan! Di pwede kulang!", "Error")
                return redirect(url_for('Student_Account'))
            
            # Update student info
            db.execute("""
                UPDATE students
                SET firstname = %s, middlename = %s, lastname = %s, age = %s, sex = %s, address = %s, 
                    cellphone_number = %s, birth_date = %s, birth_place = %s, username = %s, password = %s
                WHERE username = %s
            """, (firstname, middlename, lastname, age, sex, address, cellphone_number, birth_date, birth_place, Username, password, username))
            Connect.commit()
            session['username'] = Username  
    
        except Exception as e:
            flash(f"An error occurred: {e}", "error")
    
        return redirect(url_for('Student_Account'))


    @app.route("/delete_account", methods=["POST"])
    def delete_account():
        if 'username' not in session:
            return redirect(url_for('Student_Login'))

        username = session['username']
        confirm_firstname = request.form.get('confirm_firstname')
        confirm_lastname = request.form.get('confirm_lastname')
        confirm_username = request.form.get('confirm_username')

        db.execute("SELECT firstname, lastname FROM students WHERE username = %s", (username,))
        actual_firstname, actual_lastname = db.fetchone()

        if (confirm_firstname != actual_firstname or confirm_lastname != actual_lastname or 
            confirm_username != username):
            flash("Confirmation details do not match.", "error")
            return redirect(url_for('Student_Account'))

        try:
            db.execute("DELETE FROM students WHERE username = %s", (username,))
            Connect.commit()
            session.pop('username', None)
        except Exception as e:
            flash(f"An error occurred: {e}", "error")

        return redirect(url_for('Home'))



if __name__ == "__main__":
    app.run(debug = True) 