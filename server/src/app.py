from pygments import lexer
from src.config.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request
from flask_cors import CORS
from src.models import db


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config) #changed this to take a parameter instead of Config
    CORS(app)
    
    
    db.init_app(app)
    with app.app_context():
        from src.routes import routes
        db.create_all()
        
        return app
    




if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)