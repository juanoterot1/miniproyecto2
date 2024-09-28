from datetime import datetime
from app import db

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=True)
    credit_limit = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, full_name, email, phone, address=None, credit_limit=0.0, created_at=None):
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.address = address
        self.credit_limit = credit_limit
        self.created_at = created_at if created_at else datetime.utcnow()

    def as_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "credit_limit": self.credit_limit,
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"<Customer {self.full_name}>"
