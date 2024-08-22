import mysql.connector 

Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "students_teachers_data"
)

db = Connect.cursor()

def ForStudentRegistration(firstname, middlename, lastname, age, address, Sex, 
            cellphone_number, Birth_date, Birth_place, Username, Password, Course):

    q = """INSERT INTO student_informations(firstname, middlename, lastname, age, address, Sex, 
            cellphone_number, Birth_date, Birth_place, username, password, Course)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    v = firstname, middlename, lastname, age, address, Sex, cellphone_number, Birth_date, Birth_place, Username, Password, Course

    db.execute(q, v)
    Connect.commit()
    return

def ForTeacherRegistration(firstname, middlename, lastname, age, address, Sex, 
            cellphone_number, Birth_date, Birth_place, Username, Password, Course):

    q = """INSERT INTO teacher_informations(firstname, middlename, lastname, age, address, Sex, 
            cellphone_number, Birth_date, Birth_place, username, password, Course)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    v = firstname, middlename, lastname, age, address, Sex, cellphone_number, Birth_date, Birth_place, Username, Password, Course

    db.execute(q, v)
    Connect.commit()
    return