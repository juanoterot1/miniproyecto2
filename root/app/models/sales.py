from datetime import datetime
from app import db

class Sale(db.Model):
    __tablename__ = 'sales'
    
    id = db.Column(db.Integer, primary_key=True)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    id_customer = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)
    id_order = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=True)

    def __init__(self, total_amount, id_customer, id_order=None):
        self.total_amount = total_amount
        self.id_customer = id_customer
        self.id_order = id_order

    def as_dict(self):
        return {
            "id": self.id,
            "sale_date": self.sale_date,
            "total_amount": self.total_amount,
            "id_customer": self.id_customer,
            "id_order": self.id_order
        }

    def __repr__(self):
        return f"<Sale {self.id}>"
