import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/crickscore'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
