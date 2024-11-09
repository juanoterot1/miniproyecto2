import logging
from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.customer_service import CustomerService
from app.utils.response import create_response

# Logger configuration
logger = logging.getLogger(__name__)

# Define the Blueprint for Customer
customer_bp = Blueprint('customers', __name__)

@customer_bp.route('/customers', methods=['POST'])
@inject
def create_customer(customer_service: CustomerService):
    """
    Endpoint to create a new customer.
    """
    try:
        data = request.get_json()

        if not data or 'full_name' not in data or 'email' not in data or 'phone' not in data:
            logger.warning("Missing required fields: 'full_name', 'email', or 'phone'")
            raise BadRequest("Missing required fields: 'full_name', 'email', or 'phone'")

        logger.info(f"Creating new customer with data: {data}")
        new_customer = customer_service.create_customer(
            full_name=data.get('full_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address'),
            credit_limit=data.get('credit_limit', 0.0)
        )

        logger.info("Customer created successfully")
        return create_response(success=True, result=new_customer.as_dict(), status=201)

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return create_response(success=False, message=str(e), status=400)

    except Exception as e:
        logger.error(f"Error creating customer: {e}", exc_info=True)
        return create_response(success=False, message="Internal server error", status=500)


@customer_bp.route('/customers/<int:customer_id>', methods=['PUT'])
@inject
def update_customer(customer_id, customer_service: CustomerService):
    """
    Endpoint to update an existing customer.
    """
    try:
        data = request.get_json()

        logger.info(f"Updating customer with ID: {customer_id}")
        updated_customer = customer_service.update_customer(
            customer_id=customer_id,
            full_name=data.get('full_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address'),
            credit_limit=data.get('credit_limit')
        )

        if not updated_customer:
            raise NotFound("Customer not found.")

        logger.info(f"Customer with ID {customer_id} updated successfully")
        return create_response(success=True, result=updated_customer.as_dict(), status=200)

    except BadRequest as e:
        logger.warning(f"Bad request: {e}")
        return create_response(success=False, message=str(e), status=400)

    except NotFound as e:
        logger.warning(f"Customer not found: {e}")
        return create_response(success=False, message=str(e), status=404)

    except Exception as e:
        logger.error(f"Error updating customer with ID {customer_id}: {e}", exc_info=True)
        return create_response(success=False, message="Internal server error", status=500)


@customer_bp.route('/customers', methods=['GET'])
@inject
def get_all_customers(customer_service: CustomerService):
    """
    Endpoint to retrieve paginated customers with optional filters.
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        filters = {
            "full_name": request.args.get('full_name'),
            "email": request.args.get('email')
        }

        customers, total = customer_service.get_customers_paginated(page, per_page, **filters)

        return create_response(success=True, result={"data": [customer.as_dict() for customer in customers], "total": total}, status=200)

    except BadRequest as e:
        logger.warning(f"Bad request: {e}")
        return create_response(success=False, message=str(e), status=400)

    except Exception as e:
        logger.error(f"Error fetching customers: {e}", exc_info=True)
        return create_response(success=False, message="Internal server error", status=500)


@customer_bp.route('/customers/<int:customer_id>', methods=['GET'])
@inject
def get_customer_by_id(customer_id, customer_service: CustomerService):
    """
    Endpoint to retrieve a customer by its ID.
    """
    try:
        logger.info(f"Fetching customer by ID: {customer_id}")
        customer = customer_service.get_customer_by_id(customer_id)

        if not customer:
            raise NotFound("Customer not found")

        logger.info("Customer fetched successfully")
        return create_response(success=True, result=customer.as_dict(), status=200)

    except NotFound as e:
        logger.warning(f"Customer not found: {e}")
        return create_response(success=False, message=str(e), status=404)

    except Exception as e:
        logger.error(f"Error fetching customer by ID {customer_id}: {e}", exc_info=True)
        return create_response(success=False, message="Internal server error", status=500)


@customer_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
@inject
def delete_customer(customer_id, customer_service: CustomerService):
    """
    Endpoint to delete an existing customer.
    """
    try:
        logger.info(f"Deleting customer with ID: {customer_id}")
        result = customer_service.delete_customer(customer_id)

        if not result:
            raise NotFound("Customer not found")

        logger.info(f"Customer with ID {customer_id} deleted successfully")
        return create_response(success=True, result={"deleted_id": customer_id}, status=200)

    except NotFound as e:
        logger.error(f"Customer not found: {e}")
        return create_response(success=False, message=str(e), status=404)

    except Exception as e:
        logger.error(f"Error deleting customer with ID {customer_id}: {e}", exc_info=True)
        return create_response(success=False, message="Internal server error", status=500)
