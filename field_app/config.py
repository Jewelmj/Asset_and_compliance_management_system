"""
Configuration management for the Field Mobile App (Streamlit).
Loads configuration from environment variables.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Field App configuration."""
    
    # API configuration
    API_URL = os.getenv('API_URL', 'http://localhost:5000')
    API_BASE_URL = f"{API_URL}/api"
    
    # Application configuration
    APP_TITLE = 'Site-Steward Field App'
    APP_ICON = '📱'
    
    # Session configuration
    SESSION_TIMEOUT_MINUTES = int(os.getenv('SESSION_TIMEOUT_MINUTES', '1440'))  # 24 hours
    
    # QR Scanner configuration
    QR_SCANNER_FPS = int(os.getenv('QR_SCANNER_FPS', '10'))
    QR_SCANNER_WIDTH = int(os.getenv('QR_SCANNER_WIDTH', '640'))
    QR_SCANNER_HEIGHT = int(os.getenv('QR_SCANNER_HEIGHT', '480'))


# Create global config instance
config = Config()
