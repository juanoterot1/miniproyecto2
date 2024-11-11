from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from sqlalchemy import func, desc
from app.extensions import db
from app.models.orders import Order
from app.models.order_items import OrderItem
from app.models.customers import Customer

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
    def get_orders_paginated(page, per_page, status=None, id_customer=None):
        query = Order.query
        if status:
            query = query.filter_by(status=status)
        if id_customer:
            query = query.filter_by(id_customer=id_customer)

        # Cambiamos la ordenación para que sea descendente
        query = query.order_by(Order.id.desc())  # Orden descendente para que el último sea el primero

        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        return paginated.items, paginated.total

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
        
    # Métodos de conteo y estadísticas
    @staticmethod
    def get_total_orders():
        return db.session.query(func.count(Order.id)).scalar()

    @staticmethod
    def get_total_completed_orders():
        return db.session.query(func.count(Order.id)).filter(Order.status == 'Completada').scalar()

    @staticmethod
    def get_total_pending_orders():
        return db.session.query(func.count(Order.id)).filter(Order.status == 'Pendiente').scalar()

    @staticmethod
    def get_top_customers_by_sales(limit=3):
        return db.session.query(
            Customer.id,
            Customer.full_name,
            func.count(Order.id).label("total_orders")
        ).join(Order, Order.id_customer == Customer.id) \
         .group_by(Customer.id) \
         .order_by(desc("total_orders")) \
         .limit(limit).all()

    @staticmethod
    def get_top_selling_products(limit=3):
        return db.session.query(
            OrderItem.id_product,
            func.sum(OrderItem.quantity).label("total_quantity")
        ).group_by(OrderItem.id_product) \
         .order_by(desc("total_quantity")) \
         .limit(limit).all()
