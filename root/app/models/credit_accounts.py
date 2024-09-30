from datetime import datetime
from app import db

class CreditAccount(db.Model):
    __tablename__ = 'credit_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    credit_balance = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    id_customer = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, credit_balance, due_date, id_customer):
        self.credit_balance = credit_balance
        self.due_date = due_date
        self.id_customer = id_customer

    def as_dict(self):
        return {
            "id": self.id,
            "credit_balance": self.credit_balance,
            "due_date": self.due_date,
            "id_customer": self.id_customer
        }

    def __repr__(self):
        return f"<CreditAccount {self.id}>"


inventory.py:
from datetime import datetime
from app import db

class Inventory(db.Model):
    __tablename__ = 'inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    restock_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, product_id, stock_quantity, restock_date=None):
        self.product_id = product_id
        self.stock_quantity = stock_quantity
        self.restock_date = restock_date

    def as_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "stock_quantity": self.stock_quantity,
            "restock_date": self.restock_date
        }

    def __repr__(self):
        return f"<Inventory {self.id}>"
