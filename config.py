import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'skinanalyzer')
    
    # Model Configuration
    MODEL_PATH = "final_specific_disease_model.keras"
    IMG_SIZE = (300, 300)
