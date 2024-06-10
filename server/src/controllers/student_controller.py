from src.models.student import Student
from sqlalchemy import Insert, Delete
from src.models import db
from flask import jsonify, Response
from src.utils.normalize_data import normalize_data

#
# Pre:---
# Post: Función convencional para insertar un nuevo estudiante.
# params: data
#  
def add_student(data):
    try:
        stmt = Insert(Student).values(student_id = data["id"], name = data["name"], surname = data["surname"])

        db.session.execute(stmt)

        db.session.commit()

        return Response(status=200)
    except:
        return Response(status=409)
   

#
# Pre:---
# Post: Método para obtener los estudiantes de la base de datos
# 
def get_students():

    students = Student.query.all()

    
    return jsonify(normalize_data(students))

#
# Pre:---
# Post: Método para borrar un estudiantes de la base de datos
# params: std_id
# 
def delete_student(std_id):
    try:

        student_to_delete = Student.query.get(std_id)

        for submission in student_to_delete.submissions:
            db.session.delete(submission)
        db.session.delete(student_to_delete)
        db.session.commit()

        return Response(status=204)
    except Exception as e:
        print("Error deleting student", e)
        return Response(status=404)
    
#
# Pre:---
# Post: Método para obtener los estudiantes de la base de datos
# params: new_data
# 
def edit_student(new_data):
    try:
        std_id = new_data["std_id"]
        student = Student.query.get(std_id)

        if "new_name" in new_data and new_data["new_name"]:
            student.name = new_data["new_name"]
        
        if "new_surname" in new_data and new_data["new_surname"]:
            student.surname = new_data["new_surname"]
        
        db.session.commit()
    
        return Response(status=200)
    except Exception as e:
        print("Error editing", e)
        return Response(status=404)


