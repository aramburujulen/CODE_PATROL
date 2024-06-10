from flask import current_app as app
import src.controllers.submission_controller as sc
import src.controllers.student_controller as stc
import src.controllers.main_controller as mc
from flask import request


#Ruta para obtener entregas
@app.route("/submissions", methods=["GET"])
def get_submissions():
    return sc.get_submissions()

#Ruta para añadir un estudiante
@app.route("/addStudent", methods=["POST"])
def add_student():
    data = request.json
    return stc.add_student(data=data)

#Ruta para obtener estudiantes
@app.route("/students", methods=["GET"])
def get_students():
    return stc.get_students()

#Ruta para borrar un estudiante
@app.route("/deleteStudent/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    return stc.delete_student(student_id)

#Ruta para añadir una entrega
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

#Ruta para procesar un zip de entregas
@app.route("/processSubmissionFolder", methods=["POST"])
def process_submission_folder():
    compare_with_db = True if  request.form["compareWithDB"] == "true" else False
    zip_file = request.files["file"]
    return mc.compare_submissions_from_folder(zip_file, compare_with_db)

#Ruta para comparar dos grupos de entregas
@app.route("/compareSubmissions", methods=["POST"])
def compare_submissions():
    data = request.json

    return mc.compare_submissions(data["ids_a"], data["ids_b"])

#Ruta para procesar borrar una entrega
@app.route("/deleteSubmission/<sub_id>", methods=["DELETE"])
def delete_submission(sub_id):
    return sc.delete_submission(sub_id)

#Ruta para filtrar entregas
@app.route("/filterSubmissions", methods=["POST"])
def filter_submissions():
    return sc.get_filtered_submissions(request.json)

#Ruta para editar un estudiante
@app.route("/editStudent", methods=["PUT"])
def edit_student():
    data = request.json

    return stc.edit_student(data)




