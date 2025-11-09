from flask import (
    request,        # To read cookies: request.cookies.get('cookie_name')
    make_response,  # To create response with cookies
    redirect,       # For redirecting users
    url_for,        # For generating URLs
    session,         # Flask's session (uses signed cookies internally)
    Blueprint, 
    render_template,
    flash
)
from app.auth import login_required
from app.forms import SignupForm, LoginForm
from app.models import db, User
from app.email_service import send_welcome_email

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return redirect('/home') # Redirect the user to the homepage because this route is not needed

@bp.route('/home')
@login_required
def home():
    return render_template('home.html')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    
    if form.validate_on_submit():
        # Extract form data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already exists. Please use a different email.', 'error')
            return render_template('signup.html', form=form)
        
        # Create new user
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        
        # Hash password before storing
        user.set_password(password)
        
        # Add user to database
        try:
            db.session.add(user)
            db.session.commit()
            
            # Log the user in automatically
            session['user_id'] = user.id
            session['user_name'] = user.full_name
            
            # Send welcome email
            email_sent = send_welcome_email(user.email, user.full_name)
            if email_sent:
                flash('Account created successfully! Welcome to Budget & Beyond! A welcome email has been sent to your inbox.', 'success')
            else:
                flash('Account created successfully! Welcome to Budget & Beyond! (Note: Welcome email could not be sent)', 'success')
            
            return redirect(url_for('main.home'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.', 'error')
            return render_template('signup.html', form=form)
    
    return render_template('signup.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            # Log the user in
            session['user_id'] = user.id
            session['user_name'] = user.full_name
            
            flash('Login successful! Welcome back!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
    
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.login'))