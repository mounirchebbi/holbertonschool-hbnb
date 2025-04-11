# config.py
import os

# Base configuration class
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Development-specific configuration using MySQL
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER', 'user_hbnb')}:"
        f"{os.getenv('DB_PASSWORD', '123456')}@"
        f"{os.getenv('DB_HOST', 'localhost')}/"
        f"{os.getenv('DB_NAME', 'Hbnb')}"
    )

# Configuration dictionary for easy access
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
