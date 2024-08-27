import mysql.connector 

Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project"
)

db = Connect.cursor()


def ForStudentRegistration_students(firstname, middlename, lastname, age, address, Sex, 
            cellphone_number, Birth_date, Birth_place, Username, Password, profile_picture, year, course_id):

    q = """INSERT INTO students(firstname, middlename, lastname, age, address, sex, 
            cellphone_number, birth_date, birth_place, username, password, profile_picture, year, course_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    v = firstname, middlename, lastname, age, address, Sex, cellphone_number, Birth_date, Birth_place, Username, Password, profile_picture, year, course_id

    db.execute(q, v)
    Connect.commit()
    return

def ForStudentRegistration_course(course_id, Course):
    q = """INSERT INTO course(course)
            VALUES (%s, %s)"""
    
    v = course_id, Course

    db.execute(q, v)
    Connect.commit()
    return
    


def ForTeacherRegistration(firstname, middlename, lastname, age, address, Sex, 
            cellphone_number, Birth_date, Birth_place, Username, Password, Department, Profile_Picture, Year, semester_id):

    q = """INSERT INTO teachers(firstname, middlename, lastname, age, address, sex, 
            cellphone_number, birth_date, birth_place, username, password, department, profile_picture, year, semester_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    v = firstname, middlename, lastname, age, address, Sex, cellphone_number, Birth_date, Birth_place, Username, Password, Department, Profile_Picture, Year, semester_id

    db.execute(q, v)
    Connect.commit()
    return

def Student_Profiles(username):
    first_name_query = "SELECT firstname FROM students WHERE username = %s"
    last_name_query = "SELECT lastname FROM students WHERE username = %s"
    year_query = "SELECT year FROM students WHERE username = %s"
    course_query = """
        SELECT c.course_name
        FROM students s
        JOIN courses c ON s.course_id = c.course_id
        WHERE s.username = %s
    """

    db.execute(first_name_query, (username,))
    first_name = db.fetchone()[0]

    db.execute(last_name_query, (username,))
    last_name = db.fetchone()[0]

    db.execute(year_query, (username,))
    year = db.fetchone()[0]

    db.execute(course_query, (username,))
    course = db.fetchone()[0]
   

    return first_name, last_name, year, course


import mysql.connector

def Update_Student_Data(firstname, middlename, lastname, age, sex, address, cellphone_number, Birth_date, Birth_place, Username, Password):
    try:
        query = """
        UPDATE students 
        SET firstname = %s, 
            middlename = %s, 
            lastname = %s, 
            age = %s, 
            sex = %s, 
            address = %s, 
            cellphone_number = %s, 
            birth_date = %s, 
            birth_place = %s, 
            password = %s
        WHERE username = %s;
        """
        
        values = (firstname, middlename, lastname, age, sex, address, cellphone_number, Birth_date, Birth_place, Password, Username)
        
        db.execute(query, values)
        
        Connect.commit()

        print("Student data updated successfully!")

    except mysql.connector.Error as error:
        print(f"Error: {error}")
        Connect.rollback() 

    finally:
        db.close()
        Connect.close()