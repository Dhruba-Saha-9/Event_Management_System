import os
import secrets
from datetime import timedelta

class Config:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    
    # Database - Use SQLite by default for easier setup, MySQL as option
    if os.environ.get('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    else:
        # Try MySQL first, fallback to SQLite
        try:
            import pymysql
            SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/event_db'
        except ImportError:
            SQLALCHEMY_DATABASE_URI = 'sqlite:///event_db.sqlite'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Application settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # QR Code settings
    QR_CODE_SIZE = 200
    
    # Pagination
    EVENTS_PER_PAGE = 10
