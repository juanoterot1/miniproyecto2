import logging
from flask_injector import inject
from werkzeug.exceptions import InternalServerError, NotFound
from app.repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)

class ProductService:

    @inject
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def create_product(self, name, description=None, price=0.0, stock=0):
        try:
            logger.info(f"Creating new product: {name}")
            return self.product_repository.create_product(name, description, price, stock)
        except Exception as e:
            logger.error(f"Error creating product: {e}")
            raise InternalServerError("An error occurred while creating the product.")

    def get_all_products(self):
        try:
            return self.product_repository.get_all_products()
        except Exception as e:
            logger.error(f"Error retrieving products: {e}")
            raise InternalServerError("An error occurred while retrieving products.")

    def get_product_by_id(self, product_id):
        try:
            product = self.product_repository.get_product_by_id(product_id)
            if not product:
                raise NotFound("Product not found")
            return product
        except Exception as e:
            logger.error(f"Error retrieving product by ID {product_id}: {e}")
            raise InternalServerError("An error occurred while retrieving the product.")

    def update_product(self, product_id, name=None, description=None, price=None, stock=None):
        try:
            updated_product = self.product_repository.update_product(
                product_id, name, description, price, stock
            )
            if not updated_product:
                raise NotFound("Product not found")
            return updated_product
        except Exception as e:
            logger.error(f"Error updating product: {e}")
            raise InternalServerError("An error occurred while updating the product.")

    def delete_product(self, product_id):
        try:
            result = self.product_repository.delete_product(product_id)
            if not result:
                raise NotFound("Product not found")
            return result
        except Exception as e:
            logger.error(f"Error deleting product: {e}")
            raise InternalServerError("An error occurred while deleting the product.")
