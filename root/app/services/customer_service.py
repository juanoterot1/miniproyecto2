import logging
from flask_injector import inject
from werkzeug.exceptions import InternalServerError, NotFound, BadRequest
from app.repositories.customer_repository import CustomerRepository

logger = logging.getLogger(__name__)

class CustomerService:

    @inject
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    def create_customer(self, full_name, email, phone, address=None, credit_limit=0.0):
        """
        Creates a new customer.

        Args:
            full_name (str): The full name of the customer.
            email (str): The email address of the customer.
            phone (str): The phone number of the customer.
            address (str): The address of the customer (optional).
            credit_limit (float): The credit limit for the customer (default: 0.0).

        Returns:
            Customer: The newly created customer object.
        """
        try:
            logger.info(f"Creating a new customer with email: {email}")
            new_customer = self.customer_repository.create_customer(full_name, email, phone, address, credit_limit)
            return new_customer
        except Exception as e:
            logger.error(f"Error creating customer: {e}")
            raise InternalServerError("An internal error occurred while creating the customer.")

    def get_all_customers(self):
        """
        Retrieves all customers.

        Returns:
            list: List of all customers.
        """
        try:
            logger.info("Fetching all customers")
            customers = self.customer_repository.get_all_customers()

            if not customers:
                logger.info("No customers found.")
                raise NotFound("No customers found.")

            return customers
        except Exception as e:
            logger.error(f"Error fetching customers: {e}")
            raise InternalServerError("An internal error occurred while fetching customers.")

    def get_customer_by_id(self, customer_id):
        """
        Retrieves a customer by its ID.

        Args:
            customer_id (int): The ID of the customer to retrieve.

        Returns:
            Customer: The customer object if found, otherwise raises NotFound.
        """
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
        """
        Updates an existing customer.

        Args:
            customer_id (int): The ID of the customer to update.
            full_name (str): Optional new full name.
            email (str): Optional new email.
            phone (str): Optional new phone number.
            address (str): Optional new address.
            credit_limit (float): Optional new credit limit.

        Returns:
            Customer: The updated customer object if found, otherwise raises NotFound.
        """
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
        """
        Deletes an existing customer.

        Args:
            customer_id (int): The ID of the customer to delete.

        Returns:
            bool: True if the customer was successfully deleted, otherwise raises NotFound.
        """
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
