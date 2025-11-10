# Budget Beyond 💰

A modern, secure web application for personal finance management with advanced user experience features.

## ✨ Key Features

### 🔐 **Secure Authentication System**
- User registration with email verification
- Password hashing using bcrypt
- Session-based authentication with decorators
- Email verification requirement for full access

### 🎨 **Dynamic User Interface**
- **Animated Navbar**: Smooth slide-in animations for dynamic page titles
- **Dark/Light Theme**: Complete theme system with localStorage persistence
- **Responsive Design**: Mobile-friendly Bootstrap 5.3.2 framework
- **Personalized Experience**: Welcome messages with user's first name

### 📧 **Email Integration**
- Flask-Mail integration with Gmail SMTP
- Automated verification emails with secure tokens
- Welcome emails upon successful verification
- Professional HTML email templates

### 🎯 **Modern UX/UI**
- Clean, professional design aesthetic
- Smooth page transitions and animations  
- Context-aware navigation (authenticated vs. unauthenticated users)
- Flash messaging system for user feedback

## 🛠️ **Technology Stack**

### **Backend**
- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM
- **Flask-WTF**: Form handling and validation
- **Flask-Mail**: Email functionality
- **bcrypt**: Secure password hashing
- **itsdangerous**: Secure token generation

### **Frontend**
- **Bootstrap 5.3.2**: Responsive CSS framework
- **Custom CSS**: Advanced animations and theming
- **Vanilla JavaScript**: Theme management and UI interactions
- **Jinja2**: Template engine for dynamic content

### **Database**
- **SQLite**: Development database (easily replaceable)
- **User Model**: Complete user management with verification status

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+
- pip (Python package manager)

### **Installation**
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install Flask Flask-SQLAlchemy Flask-WTF Flask-Mail bcrypt itsdangerous
   ```
3. Run the application:
   ```bash
   python run.py
   ```
4. Open your browser to `http://127.0.0.1:5000`

### **Email Configuration**
To enable email functionality, configure your Gmail SMTP settings in the application configuration.

## 📁 **Project Structure**

```
Budget-Beyond/
├── app/                          # Main application package
│   ├── __init__.py              # App factory and configuration
│   ├── models.py                # Database models (User)
│   ├── forms.py                 # WTF-Forms for user input
│   ├── routes.py                # Application routes and logic
│   ├── auth.py                  # Authentication decorators
│   ├── email_service.py         # Email sending functionality
│   ├── static/                  # Static assets
│   │   └── css/
│   │       └── styles.css       # Custom styles with animations
│   └── templates/               # Jinja2 templates
│       ├── layout.html          # Base template with navbar
│       ├── home.html            # Dashboard/welcome page
│       ├── login.html           # User login form
│       ├── signup.html          # User registration form
│       ├── settings.html        # User settings with theme toggle
│       └── verify_email_notice.html # Email verification page
├── instance/                    # Instance-specific files
├── run.py                       # Application entry point
└── README.md                    # Project documentation
```

## 🎭 **Animation System**

### **Navbar Dynamic Animation**
- Only the dynamic portion (after "Budget Beyond") slides in/out
- Smooth single-motion animations without bounce effects
- Example: "Budget Beyond" + " - Welcome Ryan" (only " - Welcome Ryan" animates)

### **Theme Transitions**
- Seamless dark/light theme switching
- Persistent theme preference using localStorage
- Smooth color transitions for all components

## 🔒 **Security Features**

### **Password Security**
- bcrypt hashing with salt
- No plain-text password storage
- Secure password verification

### **Email Verification**
- Signed tokens with expiration
- Required for full account access
- Prevents unauthorized account creation

### **Session Management**
- Secure session handling
- Authentication state tracking
- Automatic redirect to appropriate pages

## 🎨 **Theming System**

### **Light Theme**
- Clean, professional white/gray color scheme
- High contrast for accessibility
- Bootstrap's default styling enhanced

### **Dark Theme**
- Rich dark backgrounds (#121212, #1e1e1e)
- Comfortable viewing in low-light environments
- Consistent styling across all components

## 🧩 **Component Architecture**

### **Modular Design**
- Blueprints for route organization
- Separated concerns (auth, forms, email, etc.)
- Reusable components and decorators

### **Template Inheritance**
- Base layout template for consistency
- Block-based content injection
- Dynamic title and navigation systems

## 🚧 **Development Notes**

### **Code Organization**
- Comprehensive comments and documentation
- Clean, readable code structure
- Version 3.0 - Cleaned & Optimized

### **Testing**
- Route testing with Flask test client
- Database integration testing
- Email functionality verification

## 📝 **Future Enhancements**

- [ ] Budget tracking and visualization
- [ ] Expense categorization
- [ ] Financial goal setting
- [ ] Data export capabilities
- [ ] Advanced reporting features

## 👥 **Contributing**

This is a personal finance management application designed for learning and practical use. Contributions and suggestions are welcome!

## 📄 **License**

This project is developed for educational and personal use.

---

**Budget Beyond** - Take control of your finances with style and security! 🚀
