from flask import Flask, request, render_template
from Database import *

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
            age = int(request.form["age"])
            address = str(request.form["address"])
            sex = sex = request.form.get("sex")
            cellphone_number = str(request.form["cellphone_number"])
            Birth_date = str(request.form["Birth_date"])
            Birth_place = str(request.form["Birth_place"])
            Username = str(request.form["Student_Username"])
            Password = str(request.form["Student_Password"])
            Course = str(request.form["Course"])


            ForStudentRegistration(
                firstname, middlename, lastname, age, address, sex, 
                cellphone_number, Birth_date, Birth_place, Username, Password, Course
            )

            x = "Registered Successfully!"
            return render_template("ForStudentRegistration.html", x = x)

        else:
            x = "Registration failed!"
            return render_template("ForStudentRegistration.html")
    
    @app.route("/")
    def Continue_here():
        pass # Change later


if __name__ == "__main__":
    app.run(debug = True)