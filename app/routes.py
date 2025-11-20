"""
=======================================================
Budget Beyond - Application Routes
=======================================================
Main routing module for the Budget Beyond web application

Features:
- User authentication and authorization
- Email verification system  
- Dynamic page titles with user personalization
- Session management
- Form handling with validation

Author: Budget Beyond Team
Version: 3.0 - Cleaned & Documented
=======================================================
"""

# Flask Core Imports
from flask import (
    request,        # Access request data (cookies, forms, etc.)
    make_response,  # Create HTTP responses with custom headers/cookies
    redirect,       # HTTP redirects to other routes
    url_for,        # Generate URLs for Flask routes
    session,        # Flask's secure session management
    Blueprint,      # Application component organization
    render_template, # Render Jinja2 templates
    flash          # Display one-time messages to users
)

# Application Imports
from app.auth import login_required, email_verification_required
from app.forms import SignupForm, SigninForm, ExpenseForm, BillForm, TaskForm
from app.models import db, User, Expense, Bill, Task
from app.email_service import send_verification_email, send_welcome_email

# Create Blueprint for main application routes
bp = Blueprint('main', __name__)

# ==========================================================================
# MAIN APPLICATION ROUTES
# ==========================================================================

@bp.route('/')
def index():
    """
    Root URL - redirects to home page
    This route exists for convenience but immediately redirects
    """
    return redirect('/home')

@bp.route('/home')
@login_required
@email_verification_required
def home():
    """
    Main dashboard/home page
    
    Requires:
    - User authentication (login_required)
    - Email verification (email_verification_required)
    
    Features:
    - Personalized welcome message with user's first name
    - Dynamic page title for navbar animation
    """
    user = User.query.get(session['user_id'])
    return render_template('home.html', user=user)

# ==========================================================================
# AUTHENTICATION ROUTES
# ==========================================================================

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User registration route
    
    GET: Display signup form
    POST: Process registration data
    
    Features:
    - Form validation using WTF-Forms
    - Email uniqueness verification
    - Password hashing with bcrypt
    - Automatic email verification system
    - Session initialization for new users
    """
    form = SignupForm()
    
    if form.validate_on_submit():
        # Extract and validate form data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        
        # Check for existing email addresses
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already exists. Please use a different email.', 'error')
            return render_template('signup.html', form=form)
        
        # Create new user instance
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        
        # Securely hash and store password
        user.set_password(password)
        
        # Attempt to save user to database
        try:
            db.session.add(user)
            db.session.commit()
            
            # Initialize user session (limited access until email verified)
            session['user_id'] = user.id
            session['user_name'] = user.full_name
            
            # Send email verification
            verification_token = user.generate_verification_token()
            email_sent = send_verification_email(user.email, user.full_name, verification_token)
            
            # Provide user feedback
            if email_sent:
                flash('Account created successfully! Please check your email and click the verification link to complete your registration.', 'info')
            else:
                flash('Account created successfully! However, we could not send the verification email. Please contact support.', 'warning')
            
            return redirect(url_for('main.verify_email_notice'))
            
        except Exception as e:
            # Handle database errors gracefully
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.', 'error')
            return render_template('signup.html', form=form)
    
    # Display form (GET request or validation failed)
    return render_template('signup.html', form=form)

@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            # Log the user in
            session['user_id'] = user.id
            session['user_name'] = user.full_name
            
            flash('Sign in successful! Welcome back!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
    
    return render_template('signin.html', form=form)

@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been signed out successfully.', 'info')
    return redirect(url_for('main.signin'))

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
        return redirect(url_for('main.signin'))
    
    if user.email_verified:
        flash('Your email has already been verified. You can now access your account.', 'info')
        return redirect(url_for('main.home'))
    
    # Verify the email
    user.email_verified = True
    db.session.commit()
    
    # Send welcome email now that email is verified
    send_welcome_email(user.email, user.full_name)
    
    flash('Email verified successfully! Welcome to Budget Beyond!', 'success')
    
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

@bp.route('/settings')
@login_required
@email_verification_required
def settings():
    """Settings page for user preferences"""
    user = User.query.get(session['user_id'])
    return render_template('settings.html', user=user)

# ==========================================================================
# FEATURE ROUTES: EXPENSES, BILLS, TASKS
# ==========================================================================

@bp.route('/expenses', methods=['GET', 'POST'])
@login_required
@email_verification_required
def expenses():
    """
    Expenses page

    Features:
    - Display list of expenses
    - Add, edit, and delete expenses
    - Visualize spending trends
    """
    user = User.query.get(session['user_id'])
    form = ExpenseForm()

    if form.validate_on_submit():
        # Create a new expense
        expense = Expense(
            user_id=user.id,
            category=form.category.data,
            amount=form.amount.data,
            date=form.date.data,
            notes=form.notes.data
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('main.expenses'))

    # Fetch all expenses for the user
    expenses = Expense.query.filter_by(user_id=user.id).all()
    return render_template('expenses.html', user=user, form=form, expenses=expenses)

@bp.route('/bills', methods=['GET', 'POST'])
@login_required
@email_verification_required
def bills():
    """
    Bills page

    Features:
    - Manage recurring bills
    - Track due dates and payment status
    - Send reminders for upcoming bills
    """
    user = User.query.get(session['user_id'])
    form = BillForm()

    if form.validate_on_submit():
        # Create a new bill
        bill = Bill(
            user_id=user.id,
            name=form.name.data,
            amount=form.amount.data,
            due_date=form.due_date.data,
            paid=(form.status.data == 'Paid')
        )
        db.session.add(bill)
        db.session.commit()
        flash('Bill added successfully!', 'success')
        return redirect(url_for('main.bills'))

    # Fetch all bills for the user
    bills = Bill.query.filter_by(user_id=user.id).all()
    return render_template('bills.html', user=user, form=form, bills=bills)

@bp.route('/tasks', methods=['GET', 'POST'])
@login_required
@email_verification_required
def tasks():
    """
    Tasks page

    Features:
    - Manage to-do lists
    - Add, edit, and delete tasks
    - Filter tasks by status or due date
    """
    user = User.query.get(session['user_id'])
    form = TaskForm()

    if form.validate_on_submit():
        # Create a new task
        task = Task(
            user_id=user.id,
            title=form.title.data,
            due_date=form.due_date.data,
            completed=False
        )
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('main.tasks'))

    # Fetch all tasks for the user
    tasks = Task.query.filter_by(user_id=user.id).all()
    return render_template('tasks.html', user=user, form=form, tasks=tasks)

@bp.route('/tasks/complete/<int:task_id>', methods=['POST'])
@login_required
@email_verification_required
def complete_task(task_id):
    """Mark a task as complete"""
    task = Task.query.get_or_404(task_id)
    if task.user_id != session['user_id']:
        abort(403)
    task.completed = True
    db.session.commit()
    flash('Task marked as complete!', 'success')
    return redirect(url_for('main.tasks'))

@bp.route('/tasks/delete/<int:task_id>', methods=['POST'])
@login_required
@email_verification_required
def delete_task(task_id):
    """Delete a task"""
    task = Task.query.get_or_404(task_id)
    if task.user_id != session['user_id']:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('main.tasks'))