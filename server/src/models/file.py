from . import db


class File(db.Model):
    file_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(20), nullable = True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.submission_id'), nullable=False)


