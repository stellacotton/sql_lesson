from flask import Flask, render_template, request, url_for, redirect
import hackbright_app

app = Flask(__name__)


@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    row = hackbright_app.get_student_by_github(student_github)
    if row:
        grades = hackbright_app.show_all_student_grades(student_github)
        html = render_template("student_info.html", first_name = row[0],
                                                    last_name = row[1],
                                                    github = row[2],
                                                    grades = grades)
        return html
    else:
        return redirect("/")

@app.route("/create_student", methods=["POST"])
def create_student():
    hackbright_app.connect_to_db()
    first_name = request.form.get("first_name")     
    last_name = request.form.get("last_name")
    github = request.form.get("github")
    if first_name and last_name and github:
        hackbright_app.make_new_student(first_name, last_name, github)

        return redirect("/student?github=%s"%github)
    else:
        return redirect("/")

@app.route("/create_project", methods=["POST"])
def create_project():
    hackbright_app.connect_to_db()
    title = request.form.get("title")
    description = request.form.get("description")
    max_grade = request.form.get("max_grade")

    if title and description and max_grade:
        hackbright_app.add_project(title, description, max_grade)
        return redirect("/project?project_title=%s"%title)
    else:
        return redirect("/")

@app.route("/project")
def get_all_grades_for_project():
    hackbright_app.connect_to_db()
    project_title = request.args.get("project_title")
    grades = hackbright_app.get_all_grades_for_project(project_title)
    html = render_template("project_grades.html", project_title = project_title,
                                                  grades = grades)
    return html

@app.route("/grade_student", methods=["POST"])
def assign_grade_student():
    hackbright_app.connect_to_db()
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    github = request.form.get("github")
    title = request.form.get("title")
    grade = request.form.get("grade")
    if github and title and grade:
        hackbright_app.assign_grade_by_github(github, title, grade)
        return redirect("/student?github=%s"%github)
    else:
        return redirect("/student?github=%s"%github)

@app.route("/")
def student_portal():
    return render_template("student_portal.html")


if __name__ == "__main__":
    app.run(debug=True)