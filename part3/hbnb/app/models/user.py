# app/models/user.py
from .base_model import BaseModel
from app.database import db  # Import db from the new module
#from app import db
from flask_bcrypt import Bcrypt  # Import directly from flask_bcrypt
bcrypt = Bcrypt()  # Initialize bcrypt here

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    places = db.relationship('Place', backref='owner', lazy='dynamic')
    reviews = db.relationship('Review', backref='author', lazy='dynamic')

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hash_password(password)  # Hash the password on initialization
        self.is_admin = is_admin

    def hash_password(self, password):
        """Hash the password before storing it."""
         #from app import bcrypt  # Import bcrypt here to avoid circulatr import

        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify if the provided password matches the hashed password."""
        #from app import bcrypt  # Import bcrypt here to avoid circulatr import
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Keep this method for compatibility with existing API responses."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
