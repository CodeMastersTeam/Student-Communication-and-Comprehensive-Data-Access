import matplotlib.pyplot as plt
import mysql.connector
from Database import *
import pandas as pd

def retrieve_grades_1styr(student_id):
    q = """SELECT * FROM student_grades WHERE student_id = %s"""
    db.execute(q, (student_id,))
    df = pd.DataFrame(db.fetchall(), columns=db.column_names)
    grades = df.iloc[:, 3]
    print(df.tail())

    sem_1_subs = """SELECT subject_name FROM subjects WHERE year_id = %s AND semester_id = 1"""
    sem_2_subs = """SELECT subject_name FROM subjects WHERE year_id = %s AND semester_id = 2"""
    db.execute(sem_1_subs, (1,))  # Assuming year_id is 1 for 1st year
    results1 = [item[0] for item in db.fetchall()]
    print(results1)
    db.execute(sem_2_subs, (1,))
    results2 = [item[0] for item in db.fetchall()]
    print(results2)

    all_subjects = results1 + results2
    print(all_subjects)

    min_length = min(len(all_subjects), len(grades))
    all_subjects = all_subjects[:min_length]
    grades = grades[:min_length]

    plt.plot(all_subjects, grades, marker='o')
    plt.title("Total Grades for First Semester")
    plt.xlabel("Subjects")
    plt.ylabel("Grades")
    plt.xticks(rotation=45) 
    plt.legend(["Grades"])
    plt.tight_layout()#
    plt.show()

    print(grades)


import matplotlib.pyplot as plt
import mysql.connector
from Database import *
import pandas as pd

def pie(student_id):
    periods = ['Prelim', 'Midterm', 'Finals']
    grades_dict = {}

    for period in periods:
        query = """SELECT grade FROM student_grades WHERE student_id = %s AND semester_id = 1 AND assessment_period = %s"""
        db.execute(query, (student_id, period))
        grades = db.fetchall()
        grades_dict[period] = [grade[0] for grade in grades]  # Assuming 'grade' is the first column

    df = pd.DataFrame(grades_dict)

    min_length = min(len(df[period]) for period in periods)
    df = df.head(min_length)

    for period in periods:
        plt.figure()
        plt.pie(df[period], labels=df.index, autopct='%1.1f%%')
        plt.title(f"Grades Distribution for {period}")
        plt.show()

    print(df)

pie(1)
