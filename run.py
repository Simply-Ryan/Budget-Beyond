from app import create_app

# Create the Flask app
app = create_app()

if __name__ == "__main__":
    # Enable debug mode so changes reload automatically
    app.run(debug=True)