from pygments import lexer
from config.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request
from flask_cors import CORS
from models import db


def start_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    CORS(app)
    
    db.init_app(app)

    
    with app.app_context():
        from routes import routes
        db.create_all()

        return app
    




if __name__ == "__main__":
    app = start_app()
    app.run(debug=True)