from .import db

class Student(db.Model):
    student_id = db.Column(db.String(10), primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    surname = db.Column(db.String(40), nullable = False)
    submissions = db.relationship("Submission", backref="student", lazy = True, cascade="all, delete")

