from datetime import datetime
from app import db

class SalesReport(db.Model):
    __tablename__ = 'sales_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String, nullable=False)
    report_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    total_sales = db.Column(db.Float, nullable=False)
    most_sold_product = db.Column(db.String, nullable=True)
    least_sold_product = db.Column(db.String, nullable=True)
    pending_collections = db.Column(db.Float, nullable=True)
    id_customer = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, report_type, total_sales, id_customer, report_date=None, most_sold_product=None, 
                 least_sold_product=None, pending_collections=None):
        self.report_type = report_type
        self.report_date = report_date if report_date else datetime.utcnow()
        self.total_sales = total_sales
        self.most_sold_product = most_sold_product
        self.least_sold_product = least_sold_product
        self.pending_collections = pending_collections
        self.id_customer = id_customer

    def as_dict(self):
        return {
            "id": self.id,
            "report_type": self.report_type,
            "report_date": self.report_date,
            "total_sales": self.total_sales,
            "most_sold_product": self.most_sold_product,
            "least_sold_product": self.least_sold_product,
            "pending_collections": self.pending_collections,
            "id_customer": self.id_customer
        }

    def __repr__(self):
        return f"<SalesReport {self.id}>"
