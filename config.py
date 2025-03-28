import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///crm.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get('FLASK_ENV') == 'development' 