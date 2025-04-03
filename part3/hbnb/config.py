# config.py
import os

# Base configuration class
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

# Development-specific configuration
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuration dictionary for easy access
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
