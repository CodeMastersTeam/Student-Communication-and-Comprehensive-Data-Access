from flask import Flask, render_template, request
from Camera import camera
app = Flask(__name__)

@app.route("/")
def Home():
    return render_template("Registration.html")

@app.route("/Registration_links", methods = ["POST", "GET"])
def Registration():
    link = request.form.get("link")
    if request.method == "POST":
        if link == "Teacher":
            return render_template("ForTeacherRegistration.html")
        elif link == "Student":
            return render_template("ForStudentRegistration.html")
    else:
        return render_template("Registration.html")


if __name__ == "__main__":
    app.run(debug = True)