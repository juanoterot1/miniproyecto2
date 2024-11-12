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

    @staticmethod
    def get_credit_accounts_paginated(page, per_page, id_customer=None, min_balance=None, max_balance=None):
        query = CreditAccount.query
        if id_customer:
            query = query.filter_by(id_customer=id_customer)
        if min_balance:
            query = query.filter(CreditAccount.credit_balance >= min_balance)
        if max_balance:
            query = query.filter(CreditAccount.credit_balance <= max_balance)
        
        # Orden descendente por id
        query = query.order_by(CreditAccount.id.desc())

        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        return paginated.items, paginated.total
