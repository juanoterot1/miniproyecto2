from flask import Blueprint, request
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError
from app.services.credit_account_service import CreditAccountService
from flask_injector import inject
from app.utils.response import create_response
import logging

# Configuración del blueprint para el controlador
credit_account_bp = Blueprint('credit_account_bp', __name__)
logger = logging.getLogger(__name__)

@credit_account_bp.route('/credit_accounts', methods=['POST'])
@inject
def create_credit_account(credit_account_service: CreditAccountService):
    """
    Crea una nueva cuenta de crédito (CreditAccount).
    """
    try:
        data = request.get_json()

        if not data or 'credit_balance' not in data or 'due_date' not in data or 'id_customer' not in data:
            raise BadRequest("Missing required fields: credit_balance, due_date, id_customer")

        credit_account = credit_account_service.create_credit_account(
            credit_balance=data['credit_balance'],
            due_date=data['due_date'],
            id_customer=data['id_customer']
        )

        return create_response(success=True, result=credit_account.as_dict(), status=201)

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return create_response(success=False, message=str(e), status=400)
    except Exception as e:
        logger.error(f"Internal error: {e}")
        return create_response(success=False, message="An internal error occurred while creating the credit account.", status=500)

@credit_account_bp.route('/credit_accounts/<int:account_id>', methods=['GET'])
@inject
def get_credit_account(credit_account_service: CreditAccountService, account_id):
    """
    Obtiene una cuenta de crédito por su ID.
    """
    try:
        credit_account = credit_account_service.get_credit_account_by_id(account_id)

        if not credit_account:
            raise NotFound(f"CreditAccount with ID {account_id} not found.")

        return create_response(success=True, result=credit_account.as_dict(), status=200)

    except NotFound as e:
        logger.error(f"Not found: {e}")
        return create_response(success=False, message=str(e), status=404)
    except Exception as e:
        logger.error(f"Internal error: {e}")
        return create_response(success=False, message="An internal error occurred while fetching the credit account.", status=500)

@credit_account_bp.route('/credit_accounts', methods=['GET'])
@inject
def get_credit_accounts_paginated(credit_account_service: CreditAccountService):
    """
    Obtiene una lista paginada de cuentas de crédito con filtros opcionales.
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        filters = {
            "id_customer": request.args.get('id_customer', type=int),
            "min_balance": request.args.get('min_balance', type=float),
            "max_balance": request.args.get('max_balance', type=float)
        }

        accounts, total = credit_account_service.get_credit_accounts_paginated(page, per_page, **filters)

        return create_response(success=True, result={"data": [account.as_dict() for account in accounts], "total": total}, status=200)

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return create_response(success=False, message=str(e), status=400)
    except Exception as e:
        logger.error(f"Internal error: {e}")
        return create_response(success=False, message="An internal error occurred while fetching credit accounts.", status=500)

@credit_account_bp.route('/credit_accounts/<int:account_id>', methods=['DELETE'])
@inject
def delete_credit_account(credit_account_service: CreditAccountService, account_id):
    """
    Elimina una cuenta de crédito por su ID.
    """
    try:
        deleted_account = credit_account_service.delete_credit_account(account_id)

        if not deleted_account:
            raise NotFound(f"CreditAccount with ID {account_id} not found.")

        return create_response(success=True, message=f"CreditAccount {account_id} deleted successfully.", status=200)

    except NotFound as e:
        logger.error(f"Not found: {e}")
        return create_response(success=False, message=str(e), status=404)
    except Exception as e:
        logger.error(f"Internal error: {e}")
        return create_response(success=False, message="An internal error occurred while deleting the credit account.", status=500)
