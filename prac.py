#import mysql.connector 
#
#Connect = mysql.connector.connect(
#    host = "localhost",
#    user = "root",
#    password = "",
#    database = "students_teachers_data"
#)
#
#db = Connect.cursor()
#
#username = "Selwyn"
#q = f"SELECT firstname from student_informations where username = '{username}'"
#
#db.execute(q)
#
#x = db.fetchone()
#print(x[0])


