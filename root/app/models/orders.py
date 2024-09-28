from datetime import datetime
from app import db

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    delivery_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String, nullable=False, default='pending')
    payment_method = db.Column(db.String, nullable=False)
    id_customer = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, payment_method, id_customer, delivery_date=None, status='pending'):
        self.payment_method = payment_method
        self.id_customer = id_customer
        self.delivery_date = delivery_date
        self.status = status

    def as_dict(self):
        return {
            "id": self.id,
            "order_date": self.order_date,
            "delivery_date": self.delivery_date,
            "status": self.status,
            "payment_method": self.payment_method,
            "id_customer": self.id_customer
        }

    def __repr__(self):
        return f"<Order {self.id}>"
