from . import db
from src.models.submission_comparison import submission_comparison



class Submission(db.Model):
    submission_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100), nullable = False)
    date = db.Column(db.DateTime, nullable = False)
    subject = db.Column(db.String(50), nullable = False)
    student_id = db.Column(db.String(10), db.ForeignKey("student.student_id"), nullable = False)
    files = db.relationship("File", backref="submission", lazy=True, cascade="all, delete")
    comparisons = db.relationship("Submission", secondary = submission_comparison, 
                                primaryjoin = (submission_comparison.c.submission_1_id == submission_id),
                                secondaryjoin = (submission_comparison.c.submission_2_id == submission_id),
                                backref = "submission_match")

    

        