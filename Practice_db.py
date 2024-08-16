import mysql.connector

X = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "students_teachers_data"
)

c = X.cursor()

c.execute("SELECT firstname FROM student_informations")

for i in c:
    print(i)