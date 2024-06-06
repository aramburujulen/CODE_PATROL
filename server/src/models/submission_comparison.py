from . import db

submission_comparison = db.Table("submission_comparison",
                                db.Column("submission_1_id", db.ForeignKey("submission.submission_id"), primary_key = True),
                                db.Column("submission_2_id", db.ForeignKey("submission.submission_id"), primary_key = True),
                                db.Column("overlap_in_s1", db.Float),
                                db.Column("overlap_in_s2", db.Float))