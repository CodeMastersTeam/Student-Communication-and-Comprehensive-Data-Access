from flask import Flask, render_template, request, session, redirect, url_for, flash
import matplotlib.pyplot as plt#
#import plotly.express as px
from Database import *
import os, random, cv2
import time
from werkzeug.utils import secure_filename
 
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'jfif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER) 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    

class Data:
    def __init__(self, name):
        self.app = Flask(name)
        self.app.config['uploads'] = UPLOAD_FOLDER
        self.app.secret_key = "Gwapo"


    def Direct_links(self):

        @self.app.route("/")
        def Home(): 
            return render_template("Home.html") # Home page

        @self.app.route("/Register")
        def Teacher_Register():
            return render_template("ForTeacherRegistration.html") # Teacher Registration page

        @self.app.route("/StudentsRegister")
        def Student_Register():
            return render_template("ForStudentRegistration.html") #Student Registration page

        @self.app.route("/StudentsLogin")
        def Student_Login():
            return render_template("ForStudentLogin.html") # Student Log In Page
    
        @self.app.route("/Login")
        def Teacher_login(): 
            return render_template("ForTeachersLogin.html") # Teacher Log In Page

        @self.app.route("/Teacher_Home_Page")
        def Teacher_Home_Page(): 
            username = session["username"]
            return render_template("Teacher_Home_Page.html")

        @self.app.route('/logout') # Log out
        def Student_logout():
            session.pop('username',None)
            return redirect(url_for("Home"))

    
        @self.app.route("/Student_Home")
        def Student_Home():
            
            username = session.get('username')
            if not username:
                return redirect(url_for('Student_Login'))
            Connect = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "for_finals_2nd_year_project"
            )

            db = Connect.cursor()

            db.execute("SELECT profile_picture FROM students WHERE username = %s", (username,))
            user = db.fetchone()
            db.close()
            Connect.close()

            profile_picture = user[0] if user and user[0] else None
            first_name, lastname, year, course = Student_Profiles(username)

            return render_template("Student_Home_Page.html", username=username, profile_picture=profile_picture,
                                                        first_name=first_name,
                                                        lastname=lastname, 
                                                        year=year, 
                                                        course=course)


        @self.app.route("/Student_Progress")
        def Student_Progress():
            username = session["username"]
            return render_template("Student_Progress.html")

        # TODO  Goal: Proper Student_Grades Viewing Routing
        @self.app.route("/Student_Grades")
        def Student_Grades():
            username = session.get("username")
            if username == None:
                return redirect(url_for("Student_logout"))
            else:
                
                Student_Subjects1 = fetch_student_grades(username, 1)
                Student_Subjects2 = fetch_student_grades(username, 2)

                return render_template("Student_Grades.html",  Student_Subjects1 = Student_Subjects1, 
                                                                Student_Subjects2 = Student_Subjects2)

        @self.app.route("/Student_Schedule")
        def Student_Schedule():
            Username = session["username"]
            return render_template("Student_Schedule.html")

        @self.app.route("/Student_Settings", methods = ["POST", "GET"])
        def Student_Settings():
            Username = session["username"]
            return render_template("Student_Settings.html")

        @self.app.route("/FreeCourse")
        def FreeCourse():
            return render_template("HomeFrontend.html")

        @self.app.route("/Machine_Learning")
        def Machine_Learning():
            return render_template("HomeFrontend.html")

        @self.app.route("/Foundational")
        def Foundational():
            return render_template("Foundational.html")

        @self.app.route("/AdvancedCourses")
        def AdvancedCourses():
            return render_template("Advanced Courses.html")

        @self.app.route("/Guides")
        def Guides():
            return render_template("Guides.html")

        @self.app.route("/Programmers")
        def Programmers():
            return render_template("Programmers.html")

        @self.app.route("/intro_ML")
        def intro_ML():
            return render_template("Introduction to machine learning.html")

        @self.app.route("/Machine_Learning_Crash_Course")
        def ml():
            return render_template("Machine_Learning_Crash_Course.html")

        @self.app.route("/Supervised_Learning")
        def Supervised_Learning():
            return render_template("Supervised-Learning.html")

        @self.app.route("/norman_portfolio")
        def norman_portfolio():
            return render_template("norman-portfolio.html")

        @self.app.route("/Pami_Portfolio")
        def Pami_Portfolio():
            return render_template("Pami-Portfolio.html")

        @self.app.route("/PINAKAGWAPO")
        def PINAKAGWAPO():
            return render_template("Selwyn-Portfolio.html")

        @self.app.route("/Dolly")
        def Dolly():
            return render_template("Dolly Mae Mape - Portfolio.html")

        @self.app.route("/Mharby")
        def Mharby():
            return render_template("Mharby-Portfolio.html")
        
        @self.app.route("/Registration_links", methods = ["POST", "GET"])
        def Registration():
            link = request.form.get("link")
            if request.method == "POST":
                if link == "Teacher":return render_template("Teachers.html")
                elif link == "Student":
                    return render_template("Students.html")
                elif link == "Main":
                    return render_template("Main.html")
            else:
                return render_template("Home.html")


        @self.app.route("/Inputs", methods=["GET", "POST"])
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
                section_name = "FC1 BSIT 1-1"

                if year == "1":
                    year = 1
                elif year == "2":
                    year = 2
                elif year == "3":
                    year = 3
                elif year == "4":
                    year = 4

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
                        password1, profile_picture, year, course_id ,section_name
                    )
                    flash("Registered successfully!", "success")
                except Exception as e:
                    flash(f"An error occurred: {e}", "error")

                return render_template("ForStudentRegistration.html")

            return render_template("ForStudentRegistration.html")



        @self.app.route("/TeacherInputs", methods = ["GET", "POST"])
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
                section_name = None

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
                cellphone_number, Birth_date, Birth_place, Username, Password1, Department, Profile_Picture, Year, semester_id, section_name)
                    flash("Registered successfully!", "success")

                return render_template("ForTeacherRegistration.html")

            else:
                return render_template("ForTeacherRegistration.html")

        @self.app.route("/StudentsLogin", methods = ["POST"])
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

        @self.app.route("/TeacherLogin", methods=["POST"])
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
        

        @self.app.route("/Teacher_Classes")
        def Teacher_Classes():
            username = session["username"]
            return render_template("Teacher_Classes.html")
        
        @self.app.route("/Teacher_Gradebook")
        def Teacher_Gradebook():
            username = session["username"]
            return render_template("/Teacher_Gradebook.html")
        
        @self.app.route("/Teacher_Schedule")
        def Teacher_Schedule():
            username = session["username"]
            return render_template("/Teacher_Schedule.html")

        @self.app.route("/Teacher_Messages")
        def Teacher_Messages():
            username = session["username"]
            return render_template("/Teacher_Messages.html")
        
        @self.app.route("/Teacher_Resources")
        def Teacher_Resources():
            username = session["username"]
            return render_template("/Teacher_Resources.html")
        

        @self.app.route("/Teacher_Settings")
        def Teacher_Settings():
            username = session["username"]
            return render_template("/Teacher_Settings.html")





        @self.app.route("/updatepass",methods=["POST","GET"])
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
        
        @self.app.route("/Forgot_Pass")
        def Forgot_Pass():
            return render_template("Forgot_Pass.html")


        @self.app.route("/TeacherRecoverPass", methods = ["POST"])
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



        @self.app.route("/delete_account", methods=["POST"])
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
                return redirect(url_for('Student_Settings'))

            try:
                db.execute("DELETE FROM students WHERE username = %s", (username,))
                Connect.commit()
                session.pop('username', None)
            except Exception as e:
                flash(f"An error occurred: {e}", "error")

            return redirect(url_for('Home'))

        @self.app.route("/View_Student_Infos", methods=['GET'])
        def view_student_infos():
            username = session.get("username")
            if not username:
                return redirect(url_for("Student_logout"))

            q = """
            SELECT students.student_id, students.firstname, students.middlename, 
                   students.lastname, students.age, students.address, students.sex, 
                   students.cellphone_number, students.birth_date, students.birth_place, 
                   students.username, students.password, students.profile_picture, 
                   students.year_id, courses.course_name 
            FROM students 
            JOIN courses ON students.course_id = courses.course_id 
            WHERE students.username = %s
            """

            db.execute(q, (username,))
            student_info = db.fetchone()

            if student_info:
                (student_id, firstname, middlename, lastname, age, address, sex, 
                 cellphone_number, birth_date, birth_place, username, password, 
                 profile_picture, year, course_name) = student_info
            else:
                firstname = middlename = lastname = age = address = sex = \
                cellphone_number = birth_date = birth_place = username = password = \
                profile_picture = year = course_name = None

            return render_template('View_Student_Info.html',    
                                   firstname=firstname,
                                   middlename=middlename,
                                   lastname=lastname,
                                   age=age,
                                   address=address,
                                   sex=sex,
                                   cellphone_number=cellphone_number,
                                   birth_date=birth_date,
                                   birth_place=birth_place,
                                   username=username,
                                   password=password,
                                   profile_picture=profile_picture,
                                   year=year,
                                   course_name=course_name)


        @self.app.route('/update_student_info', methods=['POST', 'GET'])
        def update_student_info():
            username = session.get('username')

            field_name = request.form.get('field_name')  
            new_value = request.form.get('new_value') 

            query = f"UPDATE students SET {field_name} = %s WHERE username = %s"
            db.execute(query, (new_value, username))

            Connect.commit()

            flash(f"{field_name.capitalize()} updated successfully.")

            return redirect(url_for('view_student_infos'))
        
        @self.app.route("/camera", methods = ['POST', 'GET']) #TODO
        def camera():
            username = session["username"]
            cam = cv2.VideoCapture(0)

            while cv2.waitKey(1) & 0xFF != ord('q'):
                ret, frame = cam.read()
                if not ret:
                    break
                
                
                cv2.imshow("Gwapo ako", frame)

                if cv2.waitKey(1) & 0xFF == ord('s'):
                    file_name = "static/New Uploads/" +str(random.randint(1, 10000)) + ".jpg" 
                    cv2.imwrite(file_name, frame)

                    img = cv2.imread(file_name)
                    cv2.imshow("New saved Image", img)

                    username = session['username']
                    query = "UPDATE students SET profile_picture = %s WHERE username = %s"
                    db.execute(query, (file_name, username))
                    Connect.commit()

                    flash("Profile picture updated successfully!")

            cam.release()
            cv2.destroyAllWindows()
            
            return render_template("View_Student_Info.html")


        @self.app.route('/upload_profile_picture', methods=['POST'])
        def upload_profile_picture():
            if 'username' not in session:
                return redirect(url_for('Student_Login'))

            file = request.files.get('profile_picture')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(self.app.config['uploads'], filename))

                username = session['username']
                query = "UPDATE students SET profile_picture = %s WHERE username = %s"
                db.execute(query, (filename, username))
                Connect.commit()

                flash("Profile picture updated successfully!")
            else:
                flash("Invalid file type. Please upload an image.")

            return redirect(url_for('view_student_infos'))

        @self.app.route("/Studentupdatepass",methods=["POST","GET"])
        def Studentupdatepass():
            if request.method == "POST":
                username = session['username']
                password1 = request.form['updatepassword1']
                password2 = request.form['updatepassword2']
                if password1 != password2:
                    flash("Password should be the same!", "error")
                    return redirect(url_for("Studentupdatepass"))

                if len(password1) < 8:
                    flash("Password should be more than 8 characters!", "error")
                    return redirect(url_for("Studentupdatepass"))
                else:
                    db.execute("UPDATE students SET password = %s WHERE username = %s",(password1,username))
                    Connect.commit()
                    flash("Updated sucessfulLy! Please log in again to continue.", "success")
            return render_template("Studentupdatepass.html")
        
        @self.app.route("/Student_Forgot_Pass")
        def Student_Forgot_Pass():
            return render_template("Student_Forgot_Pass.html")


        @self.app.route("/Student_RecoverPass", methods = ["POST"])
        def Student_RecoverPass():
            userrname = request.form["username"]
            db.execute(f"SELECT * FROM students WHERE username = '{userrname}'")
            user = db.fetchone()
            if user != None:
                session["username"] = userrname
                return redirect(url_for("Studentupdatepass"))
            else:
                flash("Email not found! Please create a new account instead", "error")
                return redirect(url_for("Student_Forgot_Pass"))

    

        @self.app.route("/Messenger", methods=["POST", "GET"])
        def Messenger():
            if "username" not in session:
                return redirect(url_for("Student_Home"))

            user = session["username"] 
            teacher_name = Teacher_Name()

            user_id = 1
            teacher_id = 1

            chat_partner_id = teacher_id if user != teacher_name else user_id  

            if request.method == "POST":
                action = request.form.get("action")

                if action == "send":
                    message = request.form.get("INpts", "").strip()
                    if not message:
                        flash("Message cannot be empty", "error")
                        return redirect(url_for("Messenger"))

                    Insert_Text_In_Messenger(user_id, chat_partner_id, message)

                elif action == "delete":
                    Delete_Text_In_Messenger(user_id, chat_partner_id)

            chat_history = Recieve_Text_In_Messenger(user_id, chat_partner_id)

            return render_template("Student_Messenger.html", x=chat_history, teacher_name=teacher_name)

        #TODO 
        @self.app.route("/Progress")
        def Progress():
            pass






    def run(self):
        self.app.run(debug = True)
        

x = Data(__name__)
x.Direct_links()
x.run()