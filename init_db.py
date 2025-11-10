#!/usr/bin/env python3

from app import create_app
from app.models import db
import os

def init_database():
    """Initialize the database with tables"""
    app = create_app()
    
    with app.app_context():
        # Remove existing database to recreate with new schema
        db_path = 'budgetbeyond.db'
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"Removed existing database: {db_path}")
        
        # Create all database tables with new schema
        db.create_all()
        print("Database tables created successfully with email verification!")
        
        # Print table info
        print(f"Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print("Tables created:")
        for table_name in db.metadata.tables.keys():
            print(f"  - {table_name}")
        
        # Show the User table schema
        print("\nUser table columns:")
        from app.models import User
        for column in User.__table__.columns:
            print(f"  - {column.name}: {column.type} {'(nullable)' if column.nullable else '(required)'}")

if __name__ == "__main__":
    init_database()