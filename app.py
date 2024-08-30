from flask import Flask, render_template, request, session, redirect, url_for, flash
import matplotlib.pyplot as plt
from Flask_links import locations
from Database import *
import os
import time
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'jfif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
app = Flask(__name__)
app.config['uploads'] = "static/uploads"


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

    @app.route("/Teacher_Home_Page")
    def Teacher_Home_Page(): 
        return render_template("Teacher_Home_Page.html") # Teacher Home Page
    
    @app.route('/logout') # Log out
    def Student_logout():
        session.pop('username',None)
        return redirect(url_for("Home"))

   
    @app.route("/Student_Home")
    def Student_Home():
        username = session.get('username')
        if not username:
            return redirect(url_for('Student_Login'))

        db.execute("SELECT profile_picture FROM students WHERE username = %s", (username,))
        user = db.fetchone()
    
        profile_picture = user[0] if user and user[0] else None
        first_name, lastname, year, course = Student_Profiles(username)

        return render_template("Student_Home_Page.html", username=username, profile_picture=profile_picture,
                                                    first_name=first_name,
                                                    lastname=lastname, 
                                                    year=year, 
                                                    course=course)


    @app.route("/Student_Progress")
    def Student_Progress():
        username = session["username"]
        return render_template("Student_Progress.html")
    
    
    @app.route("/Student_Grades")
    def Student_Grades():
        username = session["username"]
        if username == None:
            return redirect(url_for("Student_logout"))
        else:
            return render_template("Student_Grades.html")
    
    @app.route("/Student_Schedule")
    def Student_Schedule():
        Username = session["username"]
        return render_template("Student_Schedule.html")
    
    @app.route("/Student_Settings", methods = ["POST", "GET"])
    def Student_Settings():
        Username = session["username"]
        return render_template("Student_Settings.html")
    
    @app.route("/FreeCourse")
    def FreeCourse():
        return render_template("HomeFrontend.html")

    @app.route("/Machine_Learning")
    def Machine_Learning():
        return render_template("HomeFrontend.html")

    @app.route("/Foundational")
    def Foundational():
        return render_template("Foundational.html")

    @app.route("/AdvancedCourses")
    def AdvancedCourses():
        return render_template("Advanced Courses.html")

    @app.route("/Guides")
    def Guides():
        return render_template("Guides.html")

    @app.route("/Programmers")
    def Programmers():
        return render_template("Programmers.html")

    @app.route("/intro_ML")
    def intro_ML():
        return render_template("Introduction_to_machine_learning.html")
    
    @app.route("/Machine_Learning_Crash_Course")
    def ml():
        return render_template("Machine_Learning_Crash_Course.html")
    
    @app.route("/Supervised_Learning")
    def Supervised_Learning():
        return render_template("Supervised-Learning.html")
    
    @app.route("/norman_portfolio")
    def norman_portfolio():
        return render_template("norman-portfolio.html")
    
    @app.route("/Pami_Portfolio")
    def Pami_Portfolio():
        return render_template("Pami-Portfolio.html")
    
    @app.route("/PINAKAGWAPO")
    def PINAKAGWAPO():
        return render_template("Selwyn-Portfolio.html")
    
    @app.route("/Dolly")
    def Dolly():
        return render_template("Dolly Mae Mape - Portfolio.html")
    
    @app.route("/Mharby")
    def Mharby():
        return render_template("Mharby-Portfolio.html")

    @app.route('/upload_profile_pic', methods=['POST', "GET"])
    def upload_profile_pic():
        if request.method == 'POST':
            if 'profile_pic' not in request.files:
                flash('No file part')
                return redirect(url_for('Student_Account'))

            file = request.files['profile_pic']

            if file.filename == '':
                flash('No selected file')
                return redirect(url_for('Student_Account'))

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{session['username']}_{int(time.time())}_{filename}"
                file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                file.save(file_path)

                query = "UPDATE students SET profile_picture = %s WHERE username = %s"
                values = (unique_filename, session['username'])
                db.execute(query, values)
                Connect.commit()

                flash('Profile picture updated successfully')
                return redirect(url_for('Student_Account'))

            flash('Invalid file type')
            return redirect(url_for('Student_Account'))

        return redirect(url_for('Student_Account'))


    
    @app.route('/Student_Account')
    def Student_Account():
        username = session.get('username')
        if not username:
            return redirect(url_for('Student_Login'))
    
        db.execute("SELECT profile_picture FROM students WHERE username = %s", (username,))
        user = db.fetchone()
    
        profile_picture = user[0] if user and user[0] else None
    
        first_name, lastname, year, course = Student_Profiles(username)
        if first_name is None:
            flash("Error fetching student profile", "error")
            return redirect(url_for('Student_Login'))
    
        return render_template('Student_Account.html', profile_picture=profile_picture, year=year, course=course)

    
    @app.route("/Chart", methods = ["POST"])
    def Chart():
        my_data = [0.20, 0.40, 0.20, 0.15, 0.05]
        my_labels = ["Quiz", "Practical exam", "Project", "Modules", "Attendance"]
        my_colors = ["lightblue", "lightsteelblue", "silver", "cyan", "gold"] 

        def format_label(pct, all_values):
        
            if pct.is_integer():
                return "{:0f}%".format(pct) 
            else:
                return "{:.0f}%".format(pct)  

        plt.pie(
            my_data,
            labels=my_labels,
            autopct=lambda pct: format_label(pct, my_data), 
            startangle=15,
            shadow=True,
            colors=my_colors, 
        )

        plt.title("My Tasks")
        plt.axis("equal") 
        plt.show()

        return redirect(url_for("Student_Home"))