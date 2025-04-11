# app/database.py
""" Debug circular import of db """
from flask_sqlalchemy import SQLAlchemy

# Instantiate SQLAlchemy db
db = SQLAlchemy()
