from flask import Flask
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

def create_app():
    # Load environment variables from .env file
    load_dotenv()
    
    app = Flask(__name__)
    
    # Basic config
    app.config['SECRET_KEY'] = 'dev'  # Replace with env variable later
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budgetbeyond.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Email configuration
    # For development - using Gmail SMTP (you can change this)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    
    # Email credentials (you'll need to set these)
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  # Will be None for testing
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') 
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@budgetbeyond.com'

    # Initialize extensions
    from app.models import db
    from app.email_service import init_mail
    
    db.init_app(app)
    migrate = Migrate(app, db)
    init_mail(app)

    # Import and register routes
    from app import routes
    app.register_blueprint(routes.bp)

    return app