import logging
from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.customer_service import CustomerService
from app.utils.api_response import ApiResponse

# Logger configuration
logger = logging.getLogger(__name__)

# Define the Blueprint for Customer
customer_bp = Blueprint('customers', __name__)

@customer_bp.route('/customers', methods=['POST'])
@inject
def create_customer(customer_service: CustomerService):
    """
    Endpoint to create a new customer.

    Body:
        JSON: Must contain 'full_name', 'email', and 'phone', optionally 'address' and 'credit_limit'.

    Returns:
        JSON: A JSON response with the details of the created customer or an error message.
    """
    try:
        data = request.get_json()

        # Validate required fields
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
        return ApiResponse.created(data=[new_customer.as_dict()])

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))

    except Exception as e:
        logger.error(f"Error creating customer: {e}", exc_info=True)  # Captura más información del error
        return ApiResponse.internal_server_error()


@customer_bp.route('/customers/<int:customer_id>', methods=['PUT'])
@inject
def update_customer(customer_id, customer_service: CustomerService):
    """
    Endpoint to update an existing customer.

    Args:
        customer_id (int): The ID of the customer to update.

    Body:
        JSON: Can contain 'full_name', 'email', 'phone', 'address', or 'credit_limit'.

    Returns:
        JSON: A JSON response with the updated customer or an error message.
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
            logger.info(f"Customer with ID {customer_id} not found.")
            raise NotFound("Customer not found.")

        logger.info(f"Customer with ID {customer_id} updated successfully")
        return ApiResponse.ok(data=[updated_customer.as_dict()])

    except BadRequest as e:
        logger.warning(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))

    except NotFound as e:
        logger.warning(f"Customer not found: {e}")
        return ApiResponse.not_found(resource="Customer", resource_id=customer_id)

    except Exception as e:
        logger.error(f"Error updating customer with ID {customer_id}: {e}", exc_info=True)
        return ApiResponse.internal_server_error()


@customer_bp.route('/customers', methods=['GET'])
@inject
def get_all_customers(customer_service: CustomerService):
    """
    Endpoint to retrieve all customers.

    Returns:
        JSON: A JSON response with a list of all customers or an error message.
    """
    try:
        logger.info("Fetching all customers")
        customers = customer_service.get_all_customers()

        return ApiResponse.ok(data=[customer.as_dict() for customer in customers])

    except NotFound as e:
        logger.warning("No customers found.")
        return ApiResponse.not_found(resource="Customers")

    except Exception as e:
        logger.error(f"Error fetching customers: {e}", exc_info=True)
        return ApiResponse.internal_server_error()


@customer_bp.route('/customers/<int:customer_id>', methods=['GET'])
@inject
def get_customer_by_id(customer_id, customer_service: CustomerService):
    """
    Endpoint to retrieve a customer by its ID.

    Args:
        customer_id (int): The ID of the customer to retrieve.

    Returns:
        JSON: A JSON response with the requested customer or an error message.
    """
    try:
        logger.info(f"Fetching customer by ID: {customer_id}")
        customer = customer_service.get_customer_by_id(customer_id)

        if not customer:
            logger.warning(f"Customer with ID {customer_id} not found.")
            raise NotFound("Customer not found")

        logger.info("Customer fetched successfully")
        return ApiResponse.ok(data=[customer.as_dict()])

    except NotFound as e:
        logger.warning(f"Customer not found: {e}")
        return ApiResponse.not_found(resource="Customer", resource_id=customer_id)

    except Exception as e:
        logger.error(f"Error fetching customer by ID {customer_id}: {e}", exc_info=True)
        return ApiResponse.internal_server_error()


@customer_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
@inject
def delete_customer(customer_id, customer_service: CustomerService):
    """
    Endpoint to delete an existing customer.

    Args:
        customer_id (int): The ID of the customer to delete.

    Returns:
        JSON: A JSON response indicating if the deletion was successful or an error message.
    """
    try:
        logger.info(f"Deleting customer with ID: {customer_id}")
        result = customer_service.delete_customer(customer_id)

        if not result:
            logger.warning(f"Customer with ID {customer_id} not found.")
            raise NotFound(f"Customer with ID {customer_id} not found")

        logger.info(f"Customer with ID {customer_id} deleted successfully")
        return ApiResponse.ok(data=[{"deleted_id": customer_id}])

    except NotFound as e:
        logger.error(f"Customer not found: {e}")
        return ApiResponse.not_found(resource="Customer", resource_id=customer_id)

    except Exception as e:
        logger.error(f"Error deleting customer with ID {customer_id}: {e}", exc_info=True)
        return ApiResponse.internal_server_error()
