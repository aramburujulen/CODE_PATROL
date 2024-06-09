
class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:YouCan@localhost:3306/codepatrol"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 900,            
        'max_overflow': 5,        
        'pool_timeout': 30,         
        'pool_recycle': 3600,
        "pool_pre_ping": True        
    }
