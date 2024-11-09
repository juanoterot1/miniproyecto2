import logging
from flask_injector import inject
from werkzeug.exceptions import InternalServerError, NotFound
from app.repositories.order_item_repository import OrderItemRepository

logger = logging.getLogger(__name__)

class OrderItemService:

    @inject
    def __init__(self, order_item_repository: OrderItemRepository):
        self.order_item_repository = order_item_repository

    def create_order_item(self, quantity, price, id_order, id_product):
        try:
            logger.info(f"Creating new order item for order ID: {id_order}")
            return self.order_item_repository.create_order_item(
                quantity, price, id_order, id_product
            )
        except Exception as e:
            logger.error(f"Error creating order item: {e}")
            raise InternalServerError("An error occurred while creating the order item.")

    def get_order_items_paginated(self, page, per_page, id_order=None):
        try:
            logger.info(f"Fetching order items with pagination: page {page}, per_page {per_page}")
            items, total = self.order_item_repository.get_order_items_paginated(page, per_page, id_order)
            return items, total
        except Exception as e:
            logger.error(f"Error fetching paginated order items: {e}")
            raise InternalServerError("An error occurred while fetching order items.")

    def get_order_item_by_id(self, order_item_id):
        try:
            order_item = self.order_item_repository.get_order_item_by_id(order_item_id)
            if not order_item:
                raise NotFound("Order item not found")
            return order_item
        except Exception as e:
            logger.error(f"Error retrieving order item by ID {order_item_id}: {e}")
            raise InternalServerError("An error occurred while retrieving the order item.")

    def delete_order_item(self, order_item_id):
        try:
            result = self.order_item_repository.delete_order_item(order_item_id)
            if not result:
                raise NotFound("Order item not found")
            return result
        except Exception as e:
            logger.error(f"Error deleting order item: {e}")
            raise InternalServerError("An error occurred while deleting the order item.")
