import mysql.connector 

Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "students_teachers_data"
)

db = Connect.cursor()


def ForStudentRegistration(firstname, middlename, lastname, age, address, Sex, 
            cellphone_number, Birth_date, Birth_place, Username, Password, Course, Year):

    q = """INSERT INTO student_informations(firstname, middlename, lastname, age, address, Sex, 
            cellphone_number, Birth_date, Birth_place, username, password, Course, Year, session)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    v = firstname, middlename, lastname, age, address, Sex, cellphone_number, Birth_date, Birth_place, Username, Password, Course, Year, "student"

    db.execute(q, v)
    Connect.commit()
    return

def ForTeacherRegistration(firstname, middlename, lastname, age, address, Sex, 
            cellphone_number, Birth_date, Birth_place, Username, Password, Course, Year):

    q = """INSERT INTO teacher_informations(firstname, middlename, lastname, age, address, Sex, 
            cellphone_number, Birth_date, Birth_place, username, password, Course, Year, session)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    v = firstname, middlename, lastname, age, address, Sex, cellphone_number, Birth_date, Birth_place, Username, Password, Course, Year, "teacher"

    db.execute(q, v)
    Connect.commit()
    return

def Student_Profiles(username):
    first_name = "SELECT firstname FROM student_informations WHERE username = %s"
    last_name = "SELECT lastname FROM student_informations WHERE username = %s"
    year = "SELECT Year FROM student_informations WHERE username = %s"
    course = "SELECT Course FROM student_informations WHERE username = %s"

    db.execute(first_name, (username,))
    first_name = db.fetchone()[0] 

    db.execute(last_name, (username,))
    last_name = db.fetchone()[0]

    db.execute(year, (username,))
    Year = db.fetchone()[0]

    db.execute(course, (username,))
    Course = db.fetchone()[0]

    return first_name, last_name, Year, Course