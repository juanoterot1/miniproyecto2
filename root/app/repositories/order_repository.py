from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.orders import Order

class OrderRepository:
    
    @staticmethod
    def create_order(payment_method, id_customer, delivery_date=None, status='pending'):
        try:
            new_order = Order(
                payment_method=payment_method,
                id_customer=id_customer,
                delivery_date=delivery_date,
                status=status
            )
            db.session.add(new_order)
            db.session.commit()
            return new_order
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_orders():
        try:
            return Order.query.all()
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_order_by_id(order_id):
        try:
            return Order.query.get(order_id)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def update_order(order_id, payment_method=None, delivery_date=None, status=None):
        try:
            order = Order.query.get(order_id)
            if order is None:
                return None

            if payment_method:
                order.payment_method = payment_method
            if delivery_date:
                order.delivery_date = delivery_date
            if status:
                order.status = status

            db.session.commit()
            return order
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_order(order_id):
        try:
            order = Order.query.get(order_id)
            if order is None:
                return None

            db.session.delete(order)
            db.session.commit()
            return order
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
