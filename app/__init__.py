from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Basic config
    app.config['SECRET_KEY'] = 'dev'  # Replace with env variable later
    app.config['DATABASE'] = 'instance/budgetbeyond.db'

    # Import and register routes
    from app import routes
    app.register_blueprint(routes.bp)

    return app