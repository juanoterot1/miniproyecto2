from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.credit_accounts import CreditAccount

class CreditAccountRepository:
    
    @staticmethod
    def create_credit_account(credit_balance, due_date, id_customer):
        try:
            new_account = CreditAccount(
                credit_balance=credit_balance,
                due_date=due_date,
                id_customer=id_customer
            )
            db.session.add(new_account)
            db.session.commit()
            return new_account
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_credit_account_by_id(account_id):
        try:
            return CreditAccount.query.get(account_id)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def delete_credit_account(account_id):
        try:
            account = CreditAccount.query.get(account_id)
            if account is None:
                return None

            db.session.delete(account)
            db.session.commit()
            return account
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
