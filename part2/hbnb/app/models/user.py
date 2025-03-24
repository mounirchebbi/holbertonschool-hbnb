# app/models/user.py
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin
        self.created_at = datetime.now()
        self.updated_at = self.created_at
    
    @classmethod
    #allows validation before instantiation of user
    def register(cls, first_name, last_name, email, password):
        return cls(first_name, last_name, email, password)
    
    def update_profile(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.updated_at = datetime.now()
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
