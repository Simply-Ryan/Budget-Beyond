from flask import Flask
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    
    # Basic config
    app.config['SECRET_KEY'] = 'dev'  # Replace with env variable later
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budgetbeyond.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    from app.models import db
    db.init_app(app)
    migrate = Migrate(app, db)

    # Import and register routes
    from app import routes
    app.register_blueprint(routes.bp)

    return app