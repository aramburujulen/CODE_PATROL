from flask import current_app as app
import controllers.submission_controller as sc
import controllers.student_controller as stc
import controllers.main_controller as mc
from flask import request

@app.route("/submissions", methods=["GET"])
def get_submissions():
    return sc.get_submissions()

@app.route("/addStudent", methods=["POST"])
def add_student():
    data = request.json
    return stc.add_student(data=data)


@app.route("/students", methods=["GET"])
def get_students():
    return stc.get_students()


@app.route("/deleteStudent/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    return stc.delete_student(student_id)

@app.route("/addSubmission", methods=["POST"])
def add_submission():
    data = {
        "student_id": request.form["student_id"],
        "name": request.form["name"],
        "subject": request.form["subject"],
        "date": request.form["date"]
    }
    zip_file = request.files["file"]

    return sc.insert_submission(data, zip_file)

@app.route("/processSubmissionFolder", methods=["POST"])
def process_submission_folder():
    zip_file = request.files["file"]
    return mc.compare_submissions_from_folder(zip_file)


@app.route("/compareSubmissions", methods=["POST"])
def compare_submissions():
    data = request.json

    return mc.compare_submissions(data["ids_a"], data["ids_b"])

@app.route("/deleteSubmission/<sub_id>", methods=["DELETE"])
def delete_submission(sub_id):
    return sc.delete_submission(sub_id)

@app.route("/filterSubmissions", methods=["POST"])
def filter_submissions():
    return sc.get_filtered_submissions(request.json)






