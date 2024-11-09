from app import db

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    id_order = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    id_product = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, quantity, price, id_order, id_product):
        self.quantity = quantity
        self.price = price
        self.id_order = id_order
        self.id_product = id_product

    def as_dict(self):
        return {
            "id": self.id,
            "quantity": self.quantity,
            "price": self.price,
            "id_order": self.id_order,
            "id_product": self.id_product
        }

    def __repr__(self):
        return f"<OrderItem {self.id}>"
