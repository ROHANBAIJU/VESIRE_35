"""
AgriScan Backend - Configuration
Centralized configuration for the API server
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Server
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / 'data'
    MODELS_DIR = BASE_DIR / 'models'
    UPLOADS_DIR = DATA_DIR / 'uploads'
    
    # Create directories if they don't exist
    DATA_DIR.mkdir(exist_ok=True)
    UPLOADS_DIR.mkdir(exist_ok=True)
    
    # Model Configuration
    MODEL_PATH = MODELS_DIR / 'agriscan_plantdoc' / 'weights' / 'best.pt'
    LABELS_PATH = BASE_DIR / 'yolo_dataset' / 'labels.txt'
    CONFIDENCE_THRESHOLD = 0.5
    IOU_THRESHOLD = 0.45
    IMG_SIZE = 640
    
    # Database
    DATABASE_PATH = DATA_DIR / 'agriscan.db'
    DATABASE_URL = f'sqlite:///{DATABASE_PATH}'
    
    # RAG Configuration
    USE_ONLINE_RAG = os.getenv('USE_ONLINE_RAG', 'False').lower() == 'true'
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    KNOWLEDGE_BASE_PATH = DATA_DIR / 'disease_knowledge.json'
    
    # API Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    
    # CORS
    CORS_ORIGINS = ['*']  # Allow all origins for development
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = DATA_DIR / 'api.log'
    
    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

config = Config()
