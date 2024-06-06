from models.student import Student
from sqlalchemy import Insert, Delete
from models import db
from flask import jsonify, Response
from utils.normalize_data import normalize_data


def add_student(data):
    try:
        stmt = Insert(Student).values(student_id = data["id"], name = data["name"], surname = data["surname"])

        db.session.execute(stmt)

        db.session.commit()

        return Response(status=200)
    except:
        return Response(status=409)
   


def get_students():

    students = Student.query.all()

    
    return jsonify(normalize_data(students))


def delete_student(std_id):
    try:
        stmt = Delete(Student).where(Student.student_id == std_id)

        db.session.execute(stmt)

        db.session.commit()

        return Response(status=204)
    except:
        return Response(status=404)
    