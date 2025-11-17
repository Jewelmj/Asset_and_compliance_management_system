"""
Configuration management for the Admin Portal (Streamlit).
Loads configuration from environment variables.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Admin Portal configuration."""
    
    # API configuration
    API_URL = os.getenv('API_URL', 'http://localhost:5000')
    API_BASE_URL = f"{API_URL}/api"
    
    # Application configuration
    APP_TITLE = 'Site-Steward Admin Portal'
    APP_ICON = '🏗️'
    
    # Session configuration
    SESSION_TIMEOUT_MINUTES = int(os.getenv('SESSION_TIMEOUT_MINUTES', '1440'))  # 24 hours
    
    # QR Code configuration
    QR_CODE_SIZE = int(os.getenv('QR_CODE_SIZE', '10'))
    QR_CODE_BORDER = int(os.getenv('QR_CODE_BORDER', '4'))


# Create global config instance
config = Config()
