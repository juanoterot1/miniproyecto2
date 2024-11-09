import logging
from flask_injector import inject
from werkzeug.exceptions import InternalServerError, NotFound
from app.repositories.sales_repository import SaleRepository

logger = logging.getLogger(__name__)

class SaleService:

    @inject
    def __init__(self, sale_repository: SaleRepository):
        self.sale_repository = sale_repository

    def create_sale(self, total_amount, id_customer, id_order=None):
        try:
            logger.info(f"Creating new sale for customer ID: {id_customer}")
            return self.sale_repository.create_sale(
                total_amount, id_customer, id_order
            )
        except Exception as e:
            logger.error(f"Error creating sale: {e}")
            raise InternalServerError("An error occurred while creating the sale.")

    def get_sales_paginated(self, page, per_page):
        try:
            logger.info(f"Fetching sales with pagination: page {page}, per_page {per_page}")
            sales, total = self.sale_repository.get_sales_paginated(page, per_page)
            return sales, total
        except Exception as e:
            logger.error(f"Error fetching paginated sales: {e}")
            raise InternalServerError("An error occurred while retrieving sales.")

    def get_sale_by_id(self, sale_id):
        try:
            sale = self.sale_repository.get_sale_by_id(sale_id)
            if not sale:
                raise NotFound("Sale not found")
            return sale
        except Exception as e:
            logger.error(f"Error retrieving sale by ID {sale_id}: {e}")
            raise InternalServerError("An error occurred while retrieving the sale.")

    def delete_sale(self, sale_id):
        try:
            result = self.sale_repository.delete_sale(sale_id)
            if not result:
                raise NotFound("Sale not found")
            return result
        except Exception as e:
            logger.error(f"Error deleting sale: {e}")
            raise InternalServerError("An error occurred while deleting the sale.")
