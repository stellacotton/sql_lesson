import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?,?,?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    return github


def get_project_by_title(title):
    query = """SELECT * FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
Title: %s
Description: %s
Max Grade: %d""" %(row[0], row[1], row[2])

def add_project(title, description, max_grade):
    query = """INSERT into Projects VALUES (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    project_title = title
    return project_title

def get_grade_for_project(first_name, last_name, project_title):
    query = """SELECT grade FROM Grades LEFT JOIN Students ON Students.github = Grades.student_github WHERE first_name = ? AND last_name = ? AND project_title = ?"""
    DB.execute(query, (first_name, last_name, project_title))
    row = DB.fetchone()
    print """\
Grade: %s""" %row[0]

def get_all_grades_for_project(project_title):
    query = """SELECT first_name, last_name, github, grade FROM Grades LEFT JOIN Students on Students.github = Grades.student_github WHERE project_title = ?"""
    DB.execute(query, (project_title,))
    rows = DB.fetchall()
    return rows

def assign_grade_student(first_name, last_name, project_title, grade):
    query = """INSERT into Grades VALUES ((SELECT github from Students left join Grades on Students.github = Grades.student_github where first_name= ? AND last_name = ?), ?, ?)"""
    DB.execute(query, (first_name, last_name, project_title, grade))
    CONN.commit()
    

def assign_grade_by_github(github, project_title, grade):
    query = """INSERT into Grades VALUES (?, ?, ?)"""
    DB.execute(query, (github, project_title, grade))
    CONN.commit()

def show_all_student_grades(github):
    query = """SELECT project_title, grade FROM Grades WHERE student_github= ?"""
    DB.execute(query, (github,))
    row = DB.fetchall()
    return row
    # for project_title, grade in row:
    #     return project_title, grade

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(",")
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project":
            get_project_by_title(*args)
        elif command == "new_project":
            add_project(*args)
        elif command == "get_grade":
            get_grade_for_project(*args)
        elif command == "give_grade":
            assign_grade_student(*args)
        elif command == "all_grades":
            show_all_student_grades(*args)
        elif command == "all_project_grades":
            get_all_grades_for_project(*args)

    CONN.close()

if __name__ == "__main__":
    main()
