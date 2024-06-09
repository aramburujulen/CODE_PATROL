

class TestConfig():
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:YouCan@localhost:3306/codepatroltest"
    SQLALCHEMY_TRACK_MODIFICATIONS = False