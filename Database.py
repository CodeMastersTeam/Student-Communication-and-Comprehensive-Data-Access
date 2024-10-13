import mysql.connector 
from mysql.connector import Error

Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project"
)

db = Connect.cursor()


def ForStudentRegistration_students(firstname, middlename, lastname, age, address, Sex, 
            cellphone_number, Birth_date, Birth_place, Username, Password, profile_picture, year, course_id, section_name):

    q = """INSERT INTO students(firstname, middlename, lastname, age, address, sex, 
            cellphone_number, birth_date, birth_place, username, password, profile_picture, year_id, course_id, section_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    v = firstname, middlename, lastname, age, address, Sex, cellphone_number, Birth_date, Birth_place, Username, Password, profile_picture, year, course_id, section_name

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
            cellphone_number, Birth_date, Birth_place, Username, Password, Department, Profile_Picture, Year, semester_id, section_name):

    q = """INSERT INTO teachers(firstname, middlename, lastname, age, address, sex, 
            cellphone_number, birth_date, birth_place, username, password, department, profile_picture, year, semester_id, section_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    v = firstname, middlename, lastname, age, address, Sex, cellphone_number, Birth_date, Birth_place, Username, Password, Department, Profile_Picture, Year, semester_id, section_name

    db.execute(q, v)
    Connect.commit()
    return

def Student_Profiles(username):
    Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project"
)

    db = Connect.cursor()
    first_name_query = "SELECT firstname FROM students WHERE username = %s"
    last_name_query = "SELECT lastname FROM students WHERE username = %s"
    year_query = "SELECT year_id FROM students WHERE username = %s"
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


def fetch_student_grades(username, semester_id):
    Connect = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="for_finals_2nd_year_project"
    )
    db = Connect.cursor()
    
    query = '''
    SELECT
        t.firstname,
        t.lastname,
        sub.subject_name,
        sub.subject_code,
        MAX(CASE WHEN sg.assessment_period = 'Prelim' THEN sg.grade ELSE NULL END) AS Prelim,
        MAX(CASE WHEN sg.assessment_period = 'Midterm' THEN sg.grade ELSE NULL END) AS Midterm,
        MAX(CASE WHEN sg.assessment_period = 'Finals' THEN sg.grade ELSE NULL END) AS Finals,
        CONCAT(t.firstname, ' ', t.lastname) AS teacher_name
    FROM students s
    JOIN subjects sub
        ON s.course_id = sub.course_id
        AND s.year_id = sub.year_id
    LEFT JOIN teachers t
        ON sub.teacher_id = t.teacher_id
    LEFT JOIN student_grades sg
        ON s.student_id = sg.student_id
        AND sg.subject_id = sub.subject_id
        AND sg.semester_id = sub.semester_id
    WHERE s.username = %s
      AND sub.semester_id = %s
      AND sub.year_id = (SELECT year_id FROM students WHERE username = %s)
    GROUP BY sub.subject_code, sub.subject_name, teacher_name
    '''
    
    db.execute(query, (username, semester_id, username))
    results = db.fetchall()

    db.close()
    Connect.close()

    return results



def Teacher_Sections_View_Students():
    Connect = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="for_finals_2nd_year_project"
    )
    db = Connect.cursor()

    q = '''  SELECT * FROM students where course_id = 1  '''
    db.execute(q)



def get_teacher_name(teacher_id):
    try:
        query = "SELECT firstname AND lastname FROM teachers WHERE teacher_id = %s"
        db.execute(query, (teacher_id,))
        result = db.fetchone()
        if result:
            return result[0]  
        return None
    except Error as e:
        print(f"Error: {e}")
        return None

def Insert_Text_In_Messenger(Teacher_ID, Student_ID, message_Text, Message_Date = None):
    q = '''INSERT INTO messages(teacher_id, student_id, message_text, message_date)
           VALUES
           (%s, %s, %s, %s)'''
    db.execute(q, (Teacher_ID, Student_ID, message_Text, Message_Date))
    Connect.commit()

def Recieve_Text_In_Messenger(Teacher_ID, Student_ID, message_Text = None, Message_Date = None):
    q = '''SELECT message_text, message_date FROM messages WHERE teacher_id = %s AND student_id = %s'''
    c = (Teacher_ID, Student_ID)
    db.execute(q, c)
    ans = db.fetchall()
    return ans

def Delete_Text_In_Messenger(Teacher_ID = None, Student_ID = None, message_Text = None, Message_Date = None):
    q = '''DELETE FROM messages'''
    c = db.execute(q)
    if c:
        pass
        #print("\n\nMessages deleted successfully!\n\n")
    else:pass
        #print("\n\nMessage is Empty!\n\n")

def Teacher_Name():
    q = '''SELECT firstname, lastname FROM teachers WHERE teacher_id = 1'''
    db.execute(q)
    res = db.fetchall()
    for i in res:
        teacher_names = f'{i[0]} {i[1]}'
        return teacher_names
    
def Student_name(id):
    q = '''SELECT firstname, lastname FROM students WHERE student_id = %s'''
    c = (id)
    db.execute(q,c)
    for i in db.fetchone():
        student_names = f'{i[0]} {i[1]}'
        return student_names
    
