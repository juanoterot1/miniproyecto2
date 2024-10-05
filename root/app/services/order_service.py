import logging
from flask_injector import inject
from werkzeug.exceptions import InternalServerError, NotFound
from app.repositories.order_repository import OrderRepository

logger = logging.getLogger(__name__)

class OrderService:

    @inject
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def create_order(self, payment_method, id_customer, delivery_date=None, status='pending'):
        try:
            logger.info(f"Creating new order for customer ID: {id_customer}")
            return self.order_repository.create_order(
                payment_method, id_customer, delivery_date, status
            )
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            raise InternalServerError("An error occurred while creating the order.")

    def get_all_orders(self):
        try:
            return self.order_repository.get_all_orders()
        except Exception as e:
            logger.error(f"Error retrieving orders: {e}")
            raise InternalServerError("An error occurred while retrieving orders.")

    def get_order_by_id(self, order_id):
        try:
            order = self.order_repository.get_order_by_id(order_id)
            if not order:
                raise NotFound("Order not found")
            return order
        except Exception as e:
            logger.error(f"Error retrieving order by ID {order_id}: {e}")
            raise InternalServerError("An error occurred while retrieving the order.")

    def update_order(self, order_id, payment_method=None, delivery_date=None, status=None):
        try:
            updated_order = self.order_repository.update_order(
                order_id, payment_method, delivery_date, status
            )
            if not updated_order:
                raise NotFound("Order not found")
            return updated_order
        except Exception as e:
            logger.error(f"Error updating order: {e}")
            raise InternalServerError("An error occurred while updating the order.")

    def delete_order(self, order_id):
        try:
            result = self.order_repository.delete_order(order_id)
            if not result:
                raise NotFound("Order not found")
            return result
        except Exception as e:
            logger.error(f"Error deleting order: {e}")
            raise InternalServerError("An error occurred while deleting the order.")
