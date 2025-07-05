#!/usr/bin/env python3
"""
Setup script for EventHub - Event Management System
This script helps initialize the database and check dependencies.
"""

import os
import sys
from config import Config

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        ('flask', 'flask'),
        ('flask_sqlalchemy', 'flask_sqlalchemy'),
        ('flask_login', 'flask_login'),
        ('flask_wtf', 'flask_wtf'),
        ('wtforms', 'wtforms'),
        ('email_validator', 'email_validator'),
        ('qrcode', 'qrcode'),
        ('pillow', 'PIL')  # Pillow uses PIL as import name
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✓ {package_name}")
        except ImportError:
            missing_packages.append(package_name)
            print(f"✗ {package_name} - MISSING")
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    return True

def setup_database():
    """Initialize the database"""
    try:
        from app import app, db
        
        with app.app_context():
            # Drop all tables and recreate them (for schema updates)
            print("Resetting database schema...")
            db.drop_all()
            db.create_all()
            print("✓ Database tables created successfully")
            
            # Check if admin user exists
            from models import Admin
            if not Admin.query.first():
                admin = Admin(username="admin")
                admin.set_password("admin123")
                db.session.add(admin)
                db.session.commit()
                print("✓ Admin user created (username: admin, password: admin123)")
            else:
                print("✓ Admin user already exists")
                
    except Exception as e:
        print(f"✗ Database setup failed: {e}")
        return False
    
    return True

def main():
    """Main setup function"""
    print("EventHub - Event Management System Setup")
    print("=" * 50)
    
    # Check dependencies
    print("\n1. Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    # Setup database
    print("\n2. Setting up database...")
    if not setup_database():
        sys.exit(1)
    
    print("\n✓ Setup completed successfully!")
    print("\nTo run the application:")
    print("  python app.py")
    print("\nThen open your browser to: http://localhost:5000")
    print("Admin login: username=admin, password=admin123")

if __name__ == "__main__":
    main() 