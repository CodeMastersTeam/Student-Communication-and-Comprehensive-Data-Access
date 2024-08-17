import mysql.connector

Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "students_teachers_data"
)

db = Connect.cursor()

def ForStudentRegistration(firstname, middlename, lastname, age, address, sex, 
            cellphone_number, Birth_date, Birth_place):
    
    q = """INSERT INTO student_informations(firstname, middlename, lastname, age, address, sex, 
            cellphone_number, Birth_date, Birth_place)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    v = firstname, middlename, lastname, age, address, sex, cellphone_number, Birth_date, Birth_place

    db.execute(q, v)
    Connect.commit()
    return
