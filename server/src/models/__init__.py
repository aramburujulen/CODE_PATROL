from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from . import student
from . import submission
from . import file
from . import submission_comparison