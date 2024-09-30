import logging
from flask_injector import inject
from werkzeug.exceptions import InternalServerError, NotFound
from app.repositories.inventory_repository import InventoryRepository

logger = logging.getLogger(__name__)

class InventoryService:

    @inject
    def __init__(self, inventory_repository: InventoryRepository):
        self.inventory_repository = inventory_repository

    def create_inventory_item(self, product_id, stock_quantity, restock_date=None):
        try:
            logger.info(f"Creating inventory item for product ID: {product_id}")
            return self.inventory_repository.create_inventory_item(
                product_id, stock_quantity, restock_date
            )
        except Exception as e:
            logger.error(f"Error creating inventory item: {e}")
            raise InternalServerError("An error occurred while creating the inventory item.")

    def get_inventory_item_by_id(self, item_id):
        try:
            item = self.inventory_repository.get_inventory_item_by_id(item_id)
            if not item:
                raise NotFound("Inventory item not found")
            return item
        except Exception as e:
            logger.error(f"Error retrieving inventory item by ID {item_id}: {e}")
            raise InternalServerError("An error occurred while retrieving the inventory item.")

    def delete_inventory_item(self, item_id):
        try:
            result = self.inventory_repository.delete_inventory_item(item_id)
            if not result:
                raise NotFound("Inventory item not found")
            return result
        except Exception as e:
            logger.error(f"Error deleting inventory item: {e}")
            raise InternalServerError("An error occurred while deleting the inventory item.")
