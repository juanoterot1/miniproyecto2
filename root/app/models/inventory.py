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
