import logging
from flask_injector import inject
from werkzeug.exceptions import InternalServerError, NotFound
from app.repositories.customer_repository import CustomerRepository

logger = logging.getLogger(__name__)

class CustomerService:

    @inject
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    def create_customer(self, full_name, email, phone, address=None, credit_limit=0.0):
        try:
            logger.info(f"Creating a new customer with email: {email}")
            new_customer = self.customer_repository.create_customer(full_name, email, phone, address, credit_limit)
            return new_customer
        except Exception as e:
            logger.error(f"Error creating customer: {e}")
            raise InternalServerError("An internal error occurred while creating the customer.")

    def get_customers_paginated(self, page, per_page, **filters):
        try:
            logger.info(f"Fetching customers with pagination: page {page}, per_page {per_page}")
            customers, total = self.customer_repository.get_customers_paginated(page, per_page, **filters)
            return customers, total
        except Exception as e:
            logger.error(f"Error fetching paginated customers: {e}")
            raise InternalServerError("An internal error occurred while fetching customers.")

    def get_customer_by_id(self, customer_id):
        try:
            logger.info(f"Fetching customer with ID: {customer_id}")
            customer = self.customer_repository.get_customer_by_id(customer_id)

            if not customer:
                logger.info(f"Customer with ID {customer_id} not found.")
                raise NotFound("Customer not found.")

            return customer
        except Exception as e:
            logger.error(f"Error fetching customer by ID {customer_id}: {e}")
            raise InternalServerError("An internal error occurred while fetching the customer.")

    def update_customer(self, customer_id, full_name=None, email=None, phone=None, address=None, credit_limit=None):
        try:
            logger.info(f"Updating customer with ID: {customer_id}")
            updated_customer = self.customer_repository.update_customer(
                customer_id, full_name, email, phone, address, credit_limit
            )

            if not updated_customer:
                logger.info(f"Customer with ID {customer_id} not found.")
                raise NotFound("Customer not found.")

            return updated_customer
        except Exception as e:
            logger.error(f"Error updating customer with ID {customer_id}: {e}")
            raise InternalServerError("An internal error occurred while updating the customer.")

    def delete_customer(self, customer_id):
        try:
            logger.info(f"Deleting customer with ID: {customer_id}")
            result = self.customer_repository.delete_customer(customer_id)

            if not result:
                logger.warning(f"Customer with ID {customer_id} not found.")
                raise NotFound(f"Customer with ID {customer_id} not found.")

            return result
        except Exception as e:
            logger.error(f"Error deleting customer with ID {customer_id}: {e}")
            raise InternalServerError("An internal error occurred while deleting the customer.")
