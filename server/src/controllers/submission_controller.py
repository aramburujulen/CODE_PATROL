from flask import jsonify, Response
from src.models.submission import Submission
from src.models.student import Student
from src.models.file import File
from sqlalchemy import Insert
from src.utils.normalize_data import normalize_data
from src.models import db
from zipfile import ZipFile
from json import dumps


#
# Pre:---
# Post: Método encargado de obtener las entregas junto a datos de su estudiante
# 
def get_submissions():

    submissions_students = db.session.query(Submission, Student).join(Student, Submission.student_id == Student.student_id).all()

    submission_data = []
    for submission, student in submissions_students:
        new_data = {
            'submission_id': submission.submission_id,
            'submission_name': submission.name,
            'submission_date': submission.date,
            'submission_subject': submission.subject,
            'student_id': student.student_id,
            'student_name': student.name,
            'student_surname': student.surname
        }

        submission_data.append(new_data)
    

    return jsonify(submission_data)

#
# Pre:---
# Post: Método para insertar una nueva entrega. Consigue los ficheros para la entrega del zip recibido. 
# params: sub_data, zip_file
# 
def insert_submission(sub_data, zip_file):
    try:
        new_submission = Submission(student_id = sub_data["student_id"], name = sub_data["name"], date = sub_data["date"], subject = sub_data["subject"])

        db.session.add(new_submission)
        db.session.commit()

        with ZipFile(zip_file, "r") as zip_pointer:
            for file_name in zip_pointer.namelist():
                if not file_name.endswith("/"):
                    with zip_pointer.open(file_name) as file:
                        try:
                            content = file.read().decode("utf-8")
                        except Exception as e:
                            print("Skipping file with invalid codification: " + file_name, e)
                            continue
                    language = file_name.split(".")[1]
                    new_file = File(name = file_name, content = content, submission_id = new_submission.submission_id, language = language)
                    db.session.add(new_file)
        db.session.commit()
        return Response(status=200)
    except Exception as e:
        print("Error inserting submissions", e)
        return Response(status=404)

#
# Pre:---
# Post: Método encargado de borrar una entrega
# params: sub_id
# 
def delete_submission(sub_id):
    try:
        submission_to_delete = Submission.query.get(sub_id)

        if not submission_to_delete:
            return Response(dumps({"error": "Submission not found"}), status=404)
        
        db.session.delete(submission_to_delete)
        db.session.commit()

        return Response(dumps({"Success": "Submission was deleted"}), status=204)
    except Exception as e:
        print("Error deleting submission", e)
        return Response(dumps({"error": "Error deleting submission"}), status=500)
    

#
# Pre:---
# Post: Función de filtro de entregas, se puede filtrar por fecha, nombre, alumno (id) y asignatura
# params: filters
# 
def get_filtered_submissions(filters):
    try:
        base_query = db.session.query(Submission, Student)
        if "init_date" in filters and filters["init_date"]:
            base_query = base_query.filter(Submission.date >= filters["init_date"])

        if "end_date" in filters and filters["end_date"]:
            base_query = base_query.filter(Submission.date <= filters["end_date"])

        if "subject" in filters and filters["subject"]:
            base_query = base_query.filter(Submission.subject == filters["subject"])

        if "name" in filters and filters["name"]:
            base_query = base_query.filter(Submission.name == filters["name"])

        if "student_id" in filters and filters["student_id"]:
            base_query = base_query.filter(Submission.student_id == filters["student_id"])
        
        
        
        base_query = base_query.join(Student, Submission.student_id == Student.student_id)
        submissions_students = base_query.all()
        submission_data = []

        for submission, student in submissions_students:
            new_data = {
                'submission_id': submission.submission_id,
                'submission_name': submission.name,
                'submission_date': submission.date,
                'submission_subject': submission.subject,
                'student_id': student.student_id,
                'student_name': student.name,
                'student_surname': student.surname
            }
            print(new_data)
            submission_data.append(new_data)

        return jsonify(submission_data)
    except Exception as e:
        print("Error filtering subs", e)
        return Response(status=500)



