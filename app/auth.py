from functools import wraps
from flask import request, redirect, url_for, session, make_response

def login_required(f):
    """
    Decorator to require login for routes (to be placed right above route functions).
    If the user is not logged in (i.e., 'user_id' not in session), they will be redirected to the login page.
    
    DO NOT use this decorator on:
    - Login page (/login)
    - Signup/registration pages (/signup, /register)
    - Landing/welcome pages
    - Password reset pages (/forgot-password, /reset-password)
    - Public content pages
    - Error pages (404, 500, etc.)
    - Static file routes
    - API endpoints that should be public
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function