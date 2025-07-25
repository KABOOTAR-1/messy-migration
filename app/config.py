import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    DB_PATH = os.getenv('DB_PATH', os.path.join(BASE_DIR, '..', 'users.db'))
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'fallback-jwt-secret')

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)   # or whatever you want
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
