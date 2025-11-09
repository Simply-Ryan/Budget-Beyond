#!/usr/bin/env python3

from app import create_app
from app.models import db

def init_database():
    """Initialize the database with tables"""
    app = create_app()
    
    with app.app_context():
        # Create all database tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Print table info
        print(f"Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print("Tables created:")
        for table_name in db.metadata.tables.keys():
            print(f"  - {table_name}")

if __name__ == "__main__":
    init_database()