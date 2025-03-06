from flask import Flask  
from flask_sqlalchemy import SQLAlchemy  
from config import Config  
from dotenv import load_dotenv  
import os  

load_dotenv()  # Load environment variables from .env  
db = SQLAlchemy()  

def create_app():  
    app = Flask(__name__)  
    app.config.from_object(Config)  

    # Initialize extensions  
    db.init_app(app)  

    # Create tables directly in the database  
    with app.app_context():  
        db.create_all()  # This will create tables if they don't already exist  

    # Register blueprints  
    from app.routes import main  
    app.register_blueprint(main)  

    return app  