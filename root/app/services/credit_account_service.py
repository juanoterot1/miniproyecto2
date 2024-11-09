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

    def get_credit_accounts_paginated(self, page, per_page, **filters):
        """
        Retrieves a paginated list of credit accounts with optional filters.
        """
        try:
            logger.info(f"Fetching credit accounts with pagination: page {page}, per_page {per_page}")
            accounts, total = self.credit_account_repository.get_credit_accounts_paginated(page, per_page, **filters)
            return accounts, total
        except Exception as e:
            logger.error(f"Error fetching paginated credit accounts: {e}")
            raise InternalServerError("An internal error occurred while fetching paginated credit accounts.")
