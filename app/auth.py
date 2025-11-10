from functools import wraps
from flask import request, redirect, url_for, session, make_response, flash

def login_required(f):
    """
    Decorator to require login for routes (to be placed right above route functions).
    If the user is not logged in (i.e., 'user_id' not in session), they will be redirected to the signin page.
    
    DO NOT use this decorator on:
    - Signin page (/signin)
    - Signup/registration pages (/signup, /register)
    - Landing/welcome pages
    - Password reset pages (/forgot-password, /reset-password)
    - Public content pages
    - Error pages (404, 500, etc.)
    - Static file routes
    - API endpoints that should be public
    - Email verification pages (/verify-email)
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('main.signin'))
        return f(*args, **kwargs)
    return decorated_function

def email_verification_required(f):
    """
    Decorator to require email verification for routes.
    Use this in addition to @login_required for routes that need verified emails.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('main.signin'))
        
        # Check if user's email is verified
        from app.models import User
        user = User.query.get(session['user_id'])
        if user and not user.email_verified:
            flash('Please verify your email address before accessing this page.', 'warning')
            return redirect(url_for('main.verify_email_notice'))
        
        return f(*args, **kwargs)
    return decorated_function