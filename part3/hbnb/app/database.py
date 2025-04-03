# app/database.py
""" Debug circular import of db """
from flask_sqlalchemy import SQLAlchemy

# Define the SQLAlchemy instance used across the app
db = SQLAlchemy()
