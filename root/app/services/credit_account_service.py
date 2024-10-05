import logging
from flask_injector import inject
from werkzeug.exceptions import InternalServerError, NotFound, BadRequest
from app.repositories.credit_account_repository import CreditAccountRepository

logger = logging.getLogger(__name__)

class CreditAccountService:

    @inject
    def __init__(self, credit_account_repository: CreditAccountRepository):
        self.credit_account_repository = credit_account_repository

    def create_credit_account(self, credit_balance, due_date, id_customer):
        """
        Creates a new credit account.

        Args:
            credit_balance (float): The credit balance of the account.
            due_date (datetime): The due date for the credit account.
            id_customer (int): The ID of the customer to which the credit account belongs.

        Returns:
            CreditAccount: The newly created credit account object.
        """
        try:
            logger.info(f"Creating a new credit account for customer ID: {id_customer}")
            new_credit_account = self.credit_account_repository.create_credit_account(
                credit_balance=credit_balance,
                due_date=due_date,
                id_customer=id_customer
            )
            return new_credit_account
        except Exception as e:
            logger.error(f"Error creating credit account: {e}")
            raise InternalServerError("An internal error occurred while creating the credit account.")

    def get_credit_account_by_id(self, account_id):
        """
        Retrieves a credit account by its ID.

        Args:
            account_id (int): The ID of the credit account to retrieve.

        Returns:
            CreditAccount: The credit account object if found, otherwise raises NotFound.
        """
        try:
            logger.info(f"Fetching credit account with ID: {account_id}")
            credit_account = self.credit_account_repository.get_credit_account_by_id(account_id)

            if not credit_account:
                logger.info(f"Credit account with ID {account_id} not found.")
                raise NotFound("Credit account not found.")

            return credit_account
        except Exception as e:
            logger.error(f"Error fetching credit account by ID {account_id}: {e}")
            raise InternalServerError("An internal error occurred while fetching the credit account.")

    def delete_credit_account(self, account_id):
        """
        Deletes an existing credit account by its ID.

        Args:
            account_id (int): The ID of the credit account to delete.

        Returns:
            bool: True if the credit account was successfully deleted, otherwise raises NotFound.
        """
        try:
            logger.info(f"Deleting credit account with ID: {account_id}")
            deleted_account = self.credit_account_repository.delete_credit_account(account_id)

            if not deleted_account:
                logger.warning(f"Credit account with ID {account_id} not found.")
                raise NotFound(f"Credit account with ID {account_id} not found.")

            return deleted_account
        except Exception as e:
            logger.error(f"Error deleting credit account with ID {account_id}: {e}")
            raise InternalServerError("An internal error occurred while deleting the credit account.")
