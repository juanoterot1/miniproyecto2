from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.sales import Sale

class SaleRepository:
    
    @staticmethod
    def create_sale(total_amount, id_customer, id_order=None):
        try:
            new_sale = Sale(
                total_amount=total_amount,
                id_customer=id_customer,
                id_order=id_order
            )
            db.session.add(new_sale)
            db.session.commit()
            return new_sale
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_sale_by_id(sale_id):
        try:
            return Sale.query.get(sale_id)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def delete_sale(sale_id):
        try:
            sale = Sale.query.get(sale_id)
            if sale is None:
                return None

            db.session.delete(sale)
            db.session.commit()
            return sale
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
