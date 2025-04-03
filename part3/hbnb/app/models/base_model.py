# app/models/base_model.py

from app.database import db
import uuid
from datetime import datetime

# Abstract base model for common attributes and methods
class BaseModel(db.Model):
    __abstract__ = True  # Prevents SQLAlchemy from creating a table for this class

    # Common fields for all models
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def save(self):
        """Optional: Persist changes to the database."""
        self.updated_at = datetime.now()
        db.session.commit()

    def update(self, data):
        """Optional: Update model attributes and save."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
