from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, FloatField, DateField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    
    email = EmailField('Email', validators=[
        DataRequired(),
        Email()
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    
    submit = SubmitField('Create Account')

class SigninForm(FlaskForm):
    email = EmailField('Email', validators=[
        DataRequired(),
        Email()
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    
    submit = SubmitField('Sign In')

class ExpenseForm(FlaskForm):
    category = SelectField('Category', choices=[
        ('Food', 'Food'),
        ('Transportation', 'Transportation'),
        ('Utilities', 'Utilities'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other')
    ], validators=[DataRequired()])

    amount = FloatField('Amount', validators=[
        DataRequired(),
        Length(min=0, message='Amount must be positive')
    ])

    date = DateField('Date', validators=[DataRequired()])

    notes = TextAreaField('Notes', validators=[Length(max=200)])

    submit = SubmitField('Add Expense')

class BillForm(FlaskForm):
    name = StringField('Bill Name', validators=[
        DataRequired(),
        Length(max=100)
    ])

    amount = FloatField('Amount', validators=[
        DataRequired(),
        Length(min=0, message='Amount must be positive')
    ])

    due_date = DateField('Due Date', validators=[DataRequired()])

    status = SelectField('Status', choices=[
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid')
    ], validators=[DataRequired()])

    submit = SubmitField('Add Bill')

class TaskForm(FlaskForm):
    title = StringField('Task Title', validators=[
        DataRequired(),
        Length(max=200)
    ])

    due_date = DateField('Due Date', validators=[DataRequired()])

    submit = SubmitField('Add Task')