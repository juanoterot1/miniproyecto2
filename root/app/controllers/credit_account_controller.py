from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError
from app.services.credit_account_service import CreditAccountService
from flask_injector import inject
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

        # Validación de los datos
        if not data or 'credit_balance' not in data or 'due_date' not in data or 'id_customer' not in data:
            raise BadRequest("Missing required fields: credit_balance, due_date, id_customer")

        # Creación de la cuenta
        credit_account = credit_account_service.create_credit_account(
            credit_balance=data['credit_balance'],
            due_date=data['due_date'],
            id_customer=data['id_customer']
        )

        return jsonify(credit_account.as_dict()), 201

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Internal error: {e}")
        raise InternalServerError("An internal error occurred while creating the credit account.")


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

        return jsonify(credit_account.as_dict()), 200

    except NotFound as e:
        logger.error(f"Not found: {e}")
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"Internal error: {e}")
        raise InternalServerError("An internal error occurred while fetching the credit account.")


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

        return jsonify({"message": f"CreditAccount {account_id} deleted successfully."}), 200

    except NotFound as e:
        logger.error(f"Not found: {e}")
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"Internal error: {e}")
        raise InternalServerError("An internal error occurred while deleting the credit account.")
