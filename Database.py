import mysql.connector 
from mysql.connector import Error

Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project"
)

db = Connect.cursor()


class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='for_finals_2nd_year_project'
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


def ForStudentRegistration_students(firstname, middlename, lastname, age, address, Sex, 
            cellphone_number, Birth_date, Birth_place, Username, Password, profile_picture, year, course_id, section_name):
    Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project"
)

    db = Connect.cursor()
    q = """INSERT INTO students(firstname, middlename, lastname, age, address, sex, 
            cellphone_number, birth_date, birth_place, username, password, profile_picture, year_id, course_id, section_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    v = firstname, middlename, lastname, age, address, Sex, cellphone_number, Birth_date, Birth_place, Username, Password, profile_picture, year, course_id, section_name

    db.execute(q, v)
    Connect.commit()
    db.close()
    Connect.close()
    return

def ForStudentRegistration_course(course_id, Course):
    Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project"
)

    db = Connect.cursor()
    q = """INSERT INTO course(course)
            VALUES (%s, %s)"""
    
    v = course_id, Course

    db.execute(q, v)
    Connect.commit()
    db.close()
    Connect.close()
    return
    


def ForTeacherRegistration(firstname, middlename, lastname, age, address, Sex, 
            cellphone_number, Birth_date, Birth_place, Username, Password, Department, Profile_Picture, Year, semester_id, section_name):

    Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project"
)

    db = Connect.cursor()

    q = """INSERT INTO teachers(firstname, middlename, lastname, age, address, sex, 
            cellphone_number, birth_date, birth_place, username, password, department, profile_picture, year, semester_id, section_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    v = firstname, middlename, lastname, age, address, Sex, cellphone_number, Birth_date, Birth_place, Username, Password, Department, Profile_Picture, Year, semester_id, section_name

    db.execute(q, v)
    Connect.commit()

    db.close()
    Connect.close()
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
    db.close()
    Connect.close()
   

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



def student_CourseID(username):
    Connect = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="for_finals_2nd_year_project"
    )
    db = Connect.cursor()

    q = '''SELECT course_id FROM students WHERE username = %s'''
    db.execute(q, (username, ))
    res = db.fetchone()
    db.close()
    Connect.close()
    return res



def student_YearID(username):
    Connect = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="for_finals_2nd_year_project"
    )
    db = Connect.cursor()

    q = '''SELECT year_id FROM students WHERE username = %s'''
    db.execute(q, (username, ))
    res = db.fetchone()
    db.close()
    Connect.close()
    return res


# TODO SUBJECTS
def subject_student_(year_id, semester_id, course_id):

    Connect = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="for_finals_2nd_year_project"
    )
    db = Connect.cursor()

    q = '''SELECT subject_name FROM subjects WHERE year_id = %s AND semester_id = %s AND course_id = %s'''
    db.execute(q, (year_id, semester_id, course_id))
    ress = db.fetchall()

    db.close()
    Connect.close()
    return ress

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

    db.close()
    Connect.close()

def get_teacher_name(teacher_id):
    Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project"
)

    db = Connect.cursor()
    try:
        query = "SELECT firstname AND lastname FROM teachers WHERE teacher_id = %s"
        db.execute(query, (teacher_id,))
        result = db.fetchone()
        db.close()
        Connect.close()
        if result:
            return result[0]  
        return None
    except Error as e:
        print(f"Error: {e}")
        return None

def Insert_Text_In_Messenger(Teacher_ID, Student_ID, message_Text, Message_Date = None, sender_type = None, teacher_username = None, student_username = None):
    Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project"
)

    db = Connect.cursor()
    q = '''INSERT INTO messages(teacher_id, student_id, message_text, message_date, sender_type, teacher_username, student_username)
           VALUES
           (%s, %s, %s, %s, %s, %s, %s)'''
    db.execute(q, (Teacher_ID, Student_ID, message_Text, Message_Date, sender_type, teacher_username, student_username))
    Connect.commit()

    db.close()
    Connect.close()

def Recieve_Text_In_Messenger(Teacher_ID, Student_ID, message_Text = None, Message_Date = None, sender_type = None, teacher_username = None, student_username = None):
    Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project"
)

    db = Connect.cursor()
    q = '''SELECT message_text, message_date FROM messages WHERE teacher_id = %s AND student_id = %s'''
    c = (Teacher_ID, Student_ID)
    db.execute(q, c)
    ans = db.fetchall()
    db.close()
    Connect.close()
    return ans

def Delete_Text_In_Messenger(Teacher_ID = None, Student_ID = None, message_Text = None, Message_Date = None):
    Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project"
)

    db = Connect.cursor()
    q = '''DELETE FROM messages WHERE teacher_username = %s AND student_username = %s'''
    db.execute(q, (Teacher_ID, Student_ID))
    Connect.commit()
    db.close()
    Connect.close()

def Teacher_Name(year, department):
    Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project"
)

    db = Connect.cursor()
    q = '''SELECT firstname, lastname FROM teachers WHERE year = %s AND department = %s'''
    db.execute(q, (year, department, ))
    res = db.fetchall()
    db.close()
    Connect.close()
    for i in res:
        teacher_names = f'{i[0]} {i[-1]}'
        return teacher_names
    

def Teacher_username(teacher_id)  -> int:
    Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project"
)

    db = Connect.cursor()
    q = '''SELECT username from teachers where teacher_id = %s'''
    db.execute(q, (teacher_id, ))
    res = db.fetchone()
    db.close()
    Connect.close()
    return res[0]


def Student_details(username):
    Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project"
)

    db = Connect.cursor()
    q = '''SELECT * FROM students WHERE username = %s'''
    c = (username, )
    db.execute(q,c)
    det = ("student_id", "firstname", "middlename", "lastname", "age", "address", "sex", "cellphone_number", "birth_date", "birth_place", "username", "password", "profile_picture", "course_id", "section_name", "year_id")
    x = db.fetchone()
    db.close()
    Connect.close()

    c = dict(zip(det, x))
    student_ID = c["student_id"]
    firstname = c['firstname']
    lastname = c['lastname']
    course_id, section_name, year_id = c["course_id"], c["section_name"], c["year_id"]
    
    return student_ID, firstname, lastname, course_id, section_name, year_id

def Teacher_details(year, department):
    Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project",
    buffered=True
)

    db = Connect.cursor(buffered=True)
    q = '''SELECT * FROM teachers WHERE year = %s AND department = %s'''
    db.execute(q, (year, department, ))
    c = ('teacher_id', 'firstname', 'middlename', 'lastname', 'age', 'address', 'sex', 'cellphone_number', 'birth_date', 'birth_place', 'username', 'password', 'department', 'profile_picture', 'year', 'semester_id', 'section_name')
    db.close()
    Connect.close()
    zz = dict(zip(c, db.fetchone()))
    
   

    teacher_id, username, firstname, lastname, department, year, semester_id, section_name = zz["teacher_id"], zz['username'], \
    zz['firstname'], zz['lastname'], zz['department'], zz['year'], zz['semester_id'], zz['section_name']

    return teacher_id, username, firstname, lastname, department, year, semester_id, section_name

def teacher_user_id(year, department):
    Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project",
    buffered=True
)

    db = Connect.cursor(buffered=True)
    q = '''SELECT teacher_id FROM teachers where year = %s AND department = %s'''
    db.execute(q, (year, department, ))
    res = db.fetchone()
    db.close()
    Connect.close()
    return res


def student_id(username):
    Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project",
    buffered=True
)

    db = Connect.cursor(buffered=True)
    q = '''SELECT student_id FROM students where username = %s'''
    db.execute(q, (username, ))
    res = db.fetchone()
    db.close()
    Connect.close()
    return res

def student_year_course_id(username):
    Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project",
    buffered=True
)
    db = Connect.cursor(buffered=True)

    q = '''SELECT year_id, course_id FROM students where username = %s'''
    db.execute(q, (username, ))
    x = db.fetchone()
    db.close()
    Connect.close()
    return x


def Student_profile_picture(username):
    Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project"
)

    db = Connect.cursor()

    q = '''SELECT profile_picture FROM students WHERE username = %s'''
    db.execute(q, (username, ))
    x = db.fetchone()[0]
    db.close()
    Connect.close()
    return x


def student_id(username):
    Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project"
    )
    
    db = Connect.cursor()

    q = '''SELECT student_id FROM students WHERE username = %s'''

    db.execute(q, (username, ))
    x = db.fetchone()[0]

    db.close()
    Connect.close()
    return x


# TODO for GRADEBOOK
def Teacher_yearID_Department(username):
    Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project"
)


    db = Connect.cursor()
    # YEAR (year_id) AND DEPARTMENT (course_id) OF TEACHER FOR STUDENTS
    q = '''SELECT year, department FROM teachers WHERE username = %s'''
    db.execute(q, (username, ))
    res = db.fetchall()
    year = res[0][0]
    depp = res[0][1]
    department = {"BSIT": 1, "NURSING": 2, "Business Administration": 3, "EDUCATION": 4, "Secondary Education": 5}
    return year, department[depp]


def Student_firstname_lastname(year_id, course_id):
    Connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "for_finals_2nd_year_project"
)
    db = Connect.cursor()
    
    q = '''SELECT s.username, s.profile_picture, s.firstname, s.lastname FROM students AS s WHERE year_id = %s AND course_id = %s'''
    db.execute(q, (year_id, course_id))

    res = db.fetchall()
    return res

year, dep = Teacher_yearID_Department("SelwynGwapo12A")

Student_firstname_lastname(year, dep)


















