from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
import matplotlib.pyplot as plt
from Database import *
import os, random, cv2
import time
from werkzeug.utils import secure_filename
from ultralytics import YOLO
import traceback
from datetime import datetime


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
            return render_template("Main.html") # Home page

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

        @self.app.route("/Teacher_Home_Page", methods = ["POST", "GET"])
        def Teacher_Home_Page(): 
            teacher_username = session['username']

            yr, crs = Teacher_yearID_Department(teacher_username)
            first_semester = 1
            second_semester = 2
            Mastery_Prelim, Approaching, Needs_help, Failing = Mastery_Approaching_NeedsHelp_Failing(first_semester, yr)
            name_first_sem = Top_Student(yr, first_semester)
            avg_clss_scr = f'{float(Average_Class_Score(first_semester, yr)[0]):.2f}'

            total_math_confidence, total_reading_confidence, total_writing_confidence, total_critical_thinking_confidence = Class_Performance_Survey_Result()

            return render_template("Teacher_Home_Page.html", 
                                   Mastery_Prelim = Mastery_Prelim, 
                                   Approaching = Approaching, 
                                   Needs_help = Needs_help, 
                                   Failing = Failing,
                                   name_first_sem = name_first_sem,
                                   avg_clss_scr = avg_clss_scr,
                                   total_math_confidence = total_math_confidence, 
                                   total_reading_confidence = total_reading_confidence, 
                                   total_writing_confidence = total_writing_confidence, 
                                   total_critical_thinking_confidence = total_critical_thinking_confidence
                                   )

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
        
        
        @self.app.route("/Student_Survey", methods=['GET', 'POST'])
        def student_Survey():
            username = session.get("username")
            if not username:
                return redirect(url_for("Student_logout"))
            
            if request.method == 'POST':
                Student_id = student_id(username)
                math_confidence = request.form.get("math_confidence") 
                reading_confidence = request.form.get('reading_confidence')
                writing_confidence = request.form.get('writing_confidence')
                critical_thinking_confidence = request.form.get('critical_thinking_confidence')
                improvement_areas = request.form.get('improvement_areas')
                learning_methods = request.form.get('learning_methods')

                Student_Survey(Student_id, math_confidence, reading_confidence, writing_confidence, critical_thinking_confidence, 
                                                                                                   improvement_areas, 
                                                                                                   learning_methods)
                
                return render_template("Student_Survey.html", math_confidence = math_confidence, 
                                                              reading_confidence = reading_confidence, 
                                                              writing_confidence = writing_confidence, 
                                                              critical_thinking_confidence = critical_thinking_confidence,
                                                              improvement_areas = improvement_areas, 
                                                              learning_methods = learning_methods)

            return render_template("Student_Survey.html")

        @self.app.route("/Student_Progress", methods=['GET'])
        def Student_Progress():
            username = session.get("username")
            if not username:
                return redirect(url_for("Student_logout"))
            
            course_id = student_CourseID(username)
            YearID = student_YearID(username)
        
            subjects = subject_student_(YearID[0], 1, course_id[0])
            if not subjects:
                return render_template("Student_Progress.html", subjects=[], five_to_last=[], show_second_charts=False)
            
            first_4 = subjects[:4]  
            five_to_last = subjects[4:] if len(subjects) > 4 else []  
            show_second_charts = len(subjects) > 4  
        
            return render_template("Student_Progress.html", subjects=first_4, five_to_last=five_to_last, show_second_charts=show_second_charts)


        @self.app.route("/Student_Grades")
        def Student_Grades():
            username = session.get("username")
            if username == None:
                return redirect(url_for("Student_logout"))
            else:
                
                Student_Subjects1 = fetch_student_grades(username, 1)
                Student_Subjects2 = fetch_student_grades(username, 2)
                
                department = {1:"BSIT", 2: "NURSING", 3: "Business Administration", 4: "EDUCATION", 5: "Secondary Education"}
            
                user = session.get("username")
                sample = student_year_course_id(user)
                y, c = sample[0], sample[1]

                teacher_name = Teacher_details(y, department[c])
    
                Teacher_Fullname = f'{teacher_name[2]} {teacher_name[3]}' 

                return render_template("Student_Grades.html",  Student_Subjects1 = Student_Subjects1, 
                                                                Student_Subjects2 = Student_Subjects2, A = Teacher_Fullname)
            
        




        #TODO  Continue here immediatly
        @self.app.route("/Student_Schdule")
        def Student_Schdule():
            username = session.get("username")
            if username == None:
                return redirect(url_for("Student_logout"))
            else:
                
                Student_Subjects1 = fetch_student_grades(username, 1)
                Student_Subjects2 = fetch_student_grades(username, 2)
                
                department = {1:"BSIT", 2: "NURSING", 3: "Business Administration", 4: "EDUCATION", 5: "Secondary Education"}
            
                user = session["username"]
                sample = student_year_course_id(user)
                y, c = sample[0], sample[1]

                teacher_name = Teacher_details(y, department[c])
    
                Teacher_Fullname = f'{teacher_name[2]} {teacher_name[3]}' 

                return render_template("Student_Grades.html",  Student_Subjects1 = Student_Subjects1, 
                                                                Student_Subjects2 = Student_Subjects2, A = Teacher_Fullname)
            
        @self.app.route("/Student_Schedule")
        def Student_Schedule():
            username = session["username"]

            db_config = {
            'user': 'root',
            'password': '',
            'host': 'localhost',
            'database': 'for_finals_2nd_year_project',
        }       
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT year_id, course_id 
                FROM students 
                WHERE username = %s
            """, (username,))
            student_info = cursor.fetchone()

            if student_info:
                year_id = student_info['year_id']
                course_id = student_info['course_id']

                cursor.execute("""
                    SELECT * 
                    FROM weekly_schedule 
                    WHERE year_id = %s AND course_id = %s
                """, (year_id, course_id))
                weekly_schedule = cursor.fetchall()

                cursor.execute("""
                    SELECT 
                        subject_code, 
                        subject_name, 
                        CASE 
                            WHEN semester_id = 1 THEN 'First Semester'
                            WHEN semester_id = 2 THEN 'Second Semester'
                            ELSE 'Unknown'
                        END AS semester,
                        year_id AS year,
                        day_of_week,
                        time_slot,
                        location
                    FROM weekly_schedule  -- Adjusted to pull directly from the updated table
                """)
                all_subjects = cursor.fetchall()
            else:
                weekly_schedule = []
                all_subjects = []

            cursor.close()
            connection.close()

            return render_template('Student_Schedule.html', weekly_schedule=weekly_schedule, all_subjects=all_subjects)




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
        
        @self.app.route('/home')
        def home():
            return render_template("Home.html")
        
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
                return render_template("Main.html")


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
            Connect = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "for_finals_2nd_year_project"
        )

            db = Connect.cursor()

            username = request.form["LoginUsername"]
            password = request.form["LoginPassword"]
            db.execute("SELECT * FROM students WHERE username = %s AND Password = %s", (username, password))
            user = db.fetchone()
            
            Connect.close()
            db.close()

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
            yr, crs = Teacher_yearID_Department(username)
            students = Student_firstname_lastname(yr, crs)
            return render_template("Teacher_Classes.html",  students = students)
        
        @self.app.route("/Teacher_Gradebook", methods=["GET", "POST"])
        def Teacher_Gradebook():
            username = session.get("username")
            if not username:
                return redirect(url_for("Student_logout"))

            year, dep = Teacher_yearID_Department(username)

            students = Student_firstname_lastname(year, dep)

            if request.method == "POST":
                selected_student_username = request.form.get('student_username')
            else:
                selected_student_username = students[0][0] if students else None

            if not selected_student_username:
                return "No students found", 404

            Student_Subjects1 = fetch_student_grades(selected_student_username, 1)
            Student_Subjects2 = fetch_student_grades(selected_student_username, 2)

            selected_student = next((student for student in students if student[0] == selected_student_username), None)

            if not selected_student:
                return "Student not found", 404

            return render_template("Teacher_Gradebook.html", 
                                   students=students, 
                                   selected_student=selected_student, 
                                   Student_Subjects1=Student_Subjects1, 
                                   Student_Subjects2=Student_Subjects2)

        @self.app.route('/update_grade', methods=['POST'])
        def update_grade():
            print("Starting update_grade function")
            try:
                subject_code = request.form.get('subject_id')
                grade_type = request.form.get('grade_type')
                grade_value = request.form.get('grade_value')
                student_username = request.form.get('student_id')
                semester_id = request.form.get('semester_id')
                year_id = request.form.get('year_id')

                print(f"Received data: Subject: {subject_code}, Type: {grade_type}, Value: {grade_value}, Student: {student_username}, Semester: {semester_id}, Year: {year_id}")

                db = Database()
                print("Database connection established")

                update_query = """
                INSERT INTO student_grades (student_id, subject_id, grade, assessment_period, semester_id, year_id)
                VALUES ((SELECT student_id FROM students WHERE username = %s),
                        (SELECT subject_id FROM subjects WHERE subject_code = %s),
                        %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE grade = VALUES(grade)
                """
                print("Executing update query")
                db.cursor.execute(update_query, (student_username, subject_code, grade_value, grade_type, semester_id, year_id))
                db.connection.commit()
                print("Query executed and committed")

                return jsonify({'success': True, 'message': 'Grade updated'})

            except Exception as e:
                print(f"Error in update_grade: {str(e)}")
                print(traceback.format_exc())
                return jsonify({'success': False, 'message': f'Error updating grade: {str(e)}'}), 500

            finally:
                if 'db' in locals():
                    db.close()
                print("update_grade function completed")



        @self.app.route("/Teacher_Messages", methods=["POST", "GET"])
        def Teacher_Messages():
            if "username" not in session:
                return redirect(url_for("Student_Home"))

            teacher_username = session['username']
            yr, crs = Teacher_yearID_Department(teacher_username)
            student_users = Student_firstname_lastname(yr, crs)

            selected_username = request.args.get("selected_username") or request.form.get("usernamess")

            if not selected_username:
                return render_template("Teacher_Messages.html",  
                                       x=None, y=None, 
                                       teacher_name=None, 
                                       student_userss=student_users,
                                       profile_pic_student=None,
                                       student_firstname=None, 
                                       student_lastname=None)

            selected_username_id = student_id(selected_username)
            if selected_username_id is None:
                flash("Student not found", "error")
                return redirect(url_for("Teacher_Messages"))

            profile_pic_student = Student_profile_picture(selected_username)
            teacher_id = Teacher_id(teacher_username)[0]
            student_firstname, student_lastname = student_first_last(selected_username)
            student_fullname = f"{student_firstname} {student_lastname}"

            if request.method == "POST":
                action = request.form.get("action")

                if action == "send":
                    message = request.form.get("INpts", "").strip()
                    if not message:
                        flash("Message cannot be empty", "error")
                        return redirect(url_for("Teacher_Messages", selected_username=selected_username))

                    sender_type = "teacher"
                    Insert_Text_In_Messenger(teacher_id, selected_username_id, message, sender_type=sender_type,
                                             teacher_username=teacher_username, student_username=selected_username)

                elif action == "delete":
                    sender_type = "teacher"
                    Delete_Text_In_Messenger(teacher_username, selected_username, sender_type)

                return redirect(url_for("Teacher_Messages", selected_username=selected_username))

            chat_history = Recieve_Text_In_Messenger(teacher_id, selected_username_id, sender_type="teacher",
                                                     teacher_username=teacher_username, student_username=selected_username)
            chat_history2 = Recieve_Text_In_Messenger(teacher_id, selected_username_id, sender_type="student",
                                                      teacher_username=teacher_username, student_username=selected_username)

            return render_template("Teacher_Messages.html",  
                                   x=chat_history, y=chat_history2,
                                   teacher_name=student_fullname,
                                   student_userss=student_users, 
                                   profile_pic_student=profile_pic_student,
                                   selected_username=selected_username,  
                                   student_firstname=student_firstname, 
                                   student_lastname=student_lastname)


        
        
        @self.app.route("/Teacher_Schedule")
        def Teacher_Schedule():
            username = session["username"]
            return render_template("/Teacher_Schedule.html")
        
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
                flash("Username not found! Please create a new account instead", "error")
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
            Connect = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "for_finals_2nd_year_project"
)              
            db = Connect.cursor()
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
            db.close()
            Connect.close()

            if student_info:
                (student_id, firstname, middlename, lastname, age, address, sex, 
                 cellphone_number, birth_date, birth_place, username, password, 
                 profile_picture, year, course_name) = student_info
                profile_picture = Student_profile_picture(username)
            else:
                firstname = middlename = lastname = age = address = sex = \
                cellphone_number = birth_date = birth_place = username = password = \
                profile_picture = year = course_name = None
                profile_picture = Student_profile_picture(username)

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

            flash(f"{field_name.capitalize()} updated successfully.", "success")

            return render_template("View_Student_Info.html")
        
        @self.app.route("/camera", methods=['POST', 'GET'])
        def camera():
            model = YOLO('yolo11n.pt')
            Connect = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "for_finals_2nd_year_project"
        )

            db = Connect.cursor()
            username = session.get("username")
            cam = cv2.VideoCapture(0)

            while cv2.waitKey(1) & 0xFF != ord('q'):
                ret, frame = cam.read()
                if not ret:
                    break

                #pred = model(frame)[0]
                #xx = pred.plot()
                #cv2.imshow("Camera", xx)
                
                cv2.imshow("Gwapo ako", frame)

                if cv2.waitKey(1) & 0xFF == ord('s'):
                    profile_picture = "static/uploads/" + str(random.randint(1, 10000)) + ".jpg" 
                    cv2.imwrite(profile_picture, frame)

                    img = cv2.imread(profile_picture)
                    cv2.imshow("New saved Image", img)

                    profile_picture = profile_picture.split('/')[-1]
                    query = "UPDATE students SET profile_picture = %s WHERE username = %s"
                    db.execute(query, (profile_picture, username))
                    Connect.commit()

            cam.release()
            cv2.destroyAllWindows()

            q = '''SELECT profile_picture FROM students WHERE username = %s'''
            db.execute(q, (username,))
            profile_picture = db.fetchone()[0]
            db.close()
            Connect.close()

            return redirect(url_for("Student_Home"))



        @self.app.route('/upload_profile_picture', methods=['POST'])
        def upload_profile_picture():
            Connect = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "for_finals_2nd_year_project"
        )

            db = Connect.cursor()
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
                db.close()
                Connect.close()


                flash("Profile picture updated successfully!", "success")
            else:
                flash("Invalid file type. Please upload an image.", "danger")

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
                    db.close()
                    Connect.close()
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
                flash("Username not found! Please create a new account instead", "error")
                return redirect(url_for("Student_Forgot_Pass"))

    
        @self.app.route("/Messenger", methods=["POST", "GET"])
        def Messenger():
            username = session['username']
            if "username" not in session:
                return redirect(url_for("Student_Home"))
            
            department = {1:"BSIT", 2: "NURSING", 3: "Business Administration", 4: "EDUCATION", 5: "Secondary Education"}
            
            user = session["username"]
            sample = student_year_course_id(user)
            y, c = sample[0], sample[1]
            print(f"year: {y}, course_id: {c}")
            print("year", sample)

            user_id = student_id(username)
            teacher_name = Teacher_details(y, department[c])

            Teacher_Fullname = f'{teacher_name[2]} {teacher_name[3]}'  
            
            teacher_ = teacher_user_id(y, department[c])
            teacher_id = teacher_[0]
            print(f"Teacher ID: {teacher_id}")

            teacher_username = Teacher_username(teacher_id)
            
            print("Teacher teacher_username: ", teacher_username)

            chat_partner_id = user_id  if teacher_id != teacher_id else user_id  

            if request.method == "POST":
                action = request.form.get("action")

                if action == "send":
                    message = request.form.get("INpts", "").strip()
                    if not message:
                        flash("Message cannot be empty", "error")
                        return redirect(url_for("Messenger"))
                    
                    sender_type = "student"
                    Insert_Text_In_Messenger(teacher_id, user_id, message, sender_type = sender_type, teacher_username = teacher_username, student_username = user)

                elif action == "delete":
                    sender_type = "student"
                    Delete_Text_In_Messenger(teacher_username, user, sender_type)
            
            sender_type = "student"
            chat_history = Recieve_Text_In_Messenger(teacher_id, user_id, sender_type = sender_type, teacher_username = teacher_username, student_username = user)

            sender_type2 = "teacher"
            chat_history2 = Recieve_Text_In_Messenger(teacher_id, user_id, sender_type = sender_type2, teacher_username = teacher_username, student_username = user)

            return render_template("Student_Messenger.html", x=chat_history, y = chat_history2, teacher_name=Teacher_Fullname)







            
    def run(self):
        self.app.run(debug = True)
        

x = Data(__name__)
x.Direct_links()
x.run()