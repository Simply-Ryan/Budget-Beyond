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
from app.auth import login_required, email_verification_required
from app.forms import SignupForm, LoginForm
from app.models import db, User
from app.email_service import send_verification_email, send_welcome_email

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return redirect('/home') # Redirect the user to the homepage because this route is not needed

@bp.route('/home')
@login_required
@email_verification_required
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
            
            # Log the user in but don't give full access until email verified
            session['user_id'] = user.id
            session['user_name'] = user.full_name
            
            # Generate verification token and send verification email
            verification_token = user.generate_verification_token()
            email_sent = send_verification_email(user.email, user.full_name, verification_token)
            
            if email_sent:
                flash('Account created successfully! Please check your email and click the verification link to complete your registration.', 'info')
            else:
                flash('Account created successfully! However, we could not send the verification email. Please contact support.', 'warning')
            
            return redirect(url_for('main.verify_email_notice'))
            
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

@bp.route('/verify-email-notice')
@login_required
def verify_email_notice():
    """Show notice that user needs to verify their email"""
    user = User.query.get(session['user_id'])
    if user and user.email_verified:
        return redirect(url_for('main.home'))
    return render_template('verify_email_notice.html', user=user)

@bp.route('/verify-email/<token>')
def verify_email(token):
    """Handle email verification when user clicks the link"""
    user = User.verify_email_token(token)
    
    if user is None:
        flash('The verification link is invalid or has expired. Please request a new one.', 'error')
        return redirect(url_for('main.login'))
    
    if user.email_verified:
        flash('Your email has already been verified. You can now access your account.', 'info')
        return redirect(url_for('main.home'))
    
    # Verify the email
    user.email_verified = True
    db.session.commit()
    
    # Send welcome email now that email is verified
    send_welcome_email(user.email, user.full_name)
    
    flash('Email verified successfully! Welcome to Budget & Beyond!', 'success')
    
    # Log them in if they're not already
    if 'user_id' not in session:
        session['user_id'] = user.id
        session['user_name'] = user.full_name
    
    return redirect(url_for('main.home'))

@bp.route('/resend-verification')
@login_required
def resend_verification():
    """Resend verification email"""
    user = User.query.get(session['user_id'])
    
    if user and user.email_verified:
        flash('Your email is already verified.', 'info')
        return redirect(url_for('main.home'))
    
    if user:
        verification_token = user.generate_verification_token()
        email_sent = send_verification_email(user.email, user.full_name, verification_token)
        
        if email_sent:
            flash('Verification email has been resent. Please check your inbox.', 'info')
        else:
            flash('Failed to send verification email. Please try again later.', 'error')
    
    return redirect(url_for('main.verify_email_notice'))