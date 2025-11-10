from flask import current_app, render_template
from flask_mail import Mail, Message
import os

mail = Mail()

def init_mail(app):
    """Initialize Flask-Mail with the app"""
    mail.init_app(app)

def send_verification_email(user_email, user_name, verification_token):
    """Send email verification email to new users"""
    try:
        # For development/testing - print to console
        if current_app.config.get('TESTING') or not current_app.config.get('MAIL_USERNAME'):
            verification_url = f"http://127.0.0.1:5000/verify-email/{verification_token}"
            print(f"\n[EMAIL] VERIFICATION EMAIL (would be sent to {user_email}):")
            print(f"Subject: Please verify your email - Budget Beyond")
            print(f"To: {user_email}")
            print(f"Verification Link: {verification_url}")
            print(f"Body: Hello {user_name}, Please click the link to verify your email address")
            print("[EMAIL] Verification email would be sent successfully!\n")
            return True
        
        # Create verification URL
        verification_url = f"http://127.0.0.1:5000/verify-email/{verification_token}"
        
        msg = Message(
            subject='Please verify your email - Budget Beyond',
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[user_email]
        )
        
        # Email body
        msg.body = f"""
Hello {user_name},

Welcome to Budget Beyond!

To complete your registration and secure your account, please verify your email address by clicking the link below:

{verification_url}

This verification link will expire in 1 hour for security reasons.

If you did not create an account with Budget Beyond, please ignore this email.

Best regards,
The Budget Beyond Team

---
This is an automated message. Please do not reply to this email.
        """
        
        # HTML version
        msg.html = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #2c3e50;">Welcome to Budget Beyond!</h2>
        
        <p>Hello <strong>{user_name}</strong>,</p>
        
        <p>Thank you for creating an account with Budget Beyond. To complete your registration and secure your account, please verify your email address.</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{verification_url}" 
               style="background-color: #3498db; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">
                Verify My Email Address
            </a>
        </div>
        
        <p><strong>Important:</strong> This verification link will expire in 1 hour for security reasons.</p>
        
        <p>If the button above doesn't work, you can copy and paste this link into your browser:</p>
        <p style="word-break: break-all; background-color: #f8f9fa; padding: 10px; border-radius: 3px;">{verification_url}</p>
        
        <p>If you did not create an account with Budget Beyond, please ignore this email.</p>
        
        <p>Best regards,<br>The Budget Beyond Team</p>
        
        <hr style="border: 1px solid #eee; margin: 20px 0;">
        <p style="font-size: 12px; color: #666;">This is an automated message. Please do not reply to this email.</p>
    </div>
</body>
</html>
        """
        
        mail.send(msg)
        return True
        
    except Exception as e:
        print(f"Failed to send verification email: {str(e)}")
        return False

def send_welcome_email(user_email, user_name):
    """Send a welcome email to users after email verification"""
    try:
        # For development/testing - print to console
        if current_app.config.get('TESTING') or not current_app.config.get('MAIL_USERNAME'):
            print(f"\n[EMAIL] WELCOME EMAIL (would be sent to {user_email}):")
            print(f"Subject: Welcome to Budget Beyond!")
            print(f"To: {user_email}")
            print(f"Body: Hello {user_name}, Your email is now verified! Welcome to Budget Beyond!")
            print("[EMAIL] Welcome email would be sent successfully!\n")
            return True
        
        msg = Message(
            subject='Welcome to Budget Beyond!',
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[user_email]
        )
        
        # Email body (you can create an HTML template later)
        msg.body = f"""
Hello {user_name},

Welcome to Budget Beyond! 🎉

Thank you for creating an account with us. You're now ready to take control of your finances and manage your budget like never before.

Here's what you can do with Budget Beyond:
• Track your expenses and income
• Set up bill reminders
• Create and manage budgets
• Monitor your financial goals

To get started, simply log in to your account at: http://127.0.0.1:5000/login

If you have any questions or need assistance, feel free to reach out to our support team.

Best regards,
The Budget Beyond Team

---
This is an automated message. Please do not reply to this email.
        """
        
        # Optional: HTML version
        msg.html = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #2c3e50;">Welcome to Budget Beyond! 🎉</h2>
        
        <p>Hello <strong>{user_name}</strong>,</p>
        
        <p>Thank you for creating an account with us. You're now ready to take control of your finances and manage your budget like never before.</p>
        
        <h3 style="color: #34495e;">Here's what you can do with Budget Beyond:</h3>
        <ul>
            <li>💰 Track your expenses and income</li>
            <li>📅 Set up bill reminders</li>
            <li>📊 Create and manage budgets</li>
            <li>🎯 Monitor your financial goals</li>
        </ul>
        
        <p>
            <a href="http://127.0.0.1:5000/login" 
               style="background-color: #3498db; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                Get Started Now
            </a>
        </p>
        
        <p>If you have any questions or need assistance, feel free to reach out to our support team.</p>
        
        <p>Best regards,<br>The Budget Beyond Team</p>
        
        <hr style="border: 1px solid #eee; margin: 20px 0;">
        <p style="font-size: 12px; color: #666;">This is an automated message. Please do not reply to this email.</p>
    </div>
</body>
</html>
        """
        
        mail.send(msg)
        return True
        
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

def send_password_reset_email(user_email, reset_token):
    """Send password reset email (for future use)"""
    try:
        msg = Message(
            subject='Password Reset - Budget Beyond',
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[user_email]
        )
        
        msg.body = f"""
Hello,

You have requested to reset your password for Budget Beyond.

Click the link below to reset your password:
http://127.0.0.1:5000/reset-password/{reset_token}

This link will expire in 1 hour for security reasons.

If you did not request this password reset, please ignore this email.

Best regards,
The Budget Beyond Team
        """
        
        mail.send(msg)
        return True
        
    except Exception as e:
        print(f"Failed to send password reset email: {str(e)}")
        return False