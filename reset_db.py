#!/usr/bin/env python3
"""
Database reset script for EventHub
This will drop all tables and recreate them with the new schema.
"""

from flask import Flask
from config import Config
from models import db, Admin

# Create a minimal Flask app for database operations
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    
    print("Creating new tables...")
    db.create_all()
    
    print("Creating admin user...")
    admin = Admin(username="admin")
    admin.set_password("admin123")
    db.session.add(admin)
    db.session.commit()
    
    print("✓ Database reset completed successfully!")
    print("Admin login: username=admin, password=admin123") 