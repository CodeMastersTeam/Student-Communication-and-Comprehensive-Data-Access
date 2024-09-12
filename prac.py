import mysql.connector

def Teacher_infos(username):
    Connect = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="for_finals_2nd_year_project"
    )
    db = Connect.cursor()

    q = '''SELECT * FROM teachers WHERE username = %s'''
    db.execute(q, (username,))

    result = db.fetchone()

    if result:
        print(result[1])
    else:
        print("No record found.")

    db.close()
    Connect.close()

Teacher_infos('SelwynGwapo12')
