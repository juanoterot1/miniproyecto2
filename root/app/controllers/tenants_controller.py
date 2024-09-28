from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.tenants_service import TenantService
from app.utils.api_response import ApiResponse
import logging

# Logger configuration
logger = logging.getLogger(__name__)

# Define the Blueprint for Tenant
tenant_bp = Blueprint('tenants', __name__)

@tenant_bp.route('/tenants', methods=['POST'])
@inject
def create_tenant(tenant_service: TenantService):
    """
    Endpoint to create a new tenant.

    Body:
        JSON:
            - tenant_name (str): The name of the tenant.
            - schema_name (str): The schema name for the tenant.

    Returns:
        JSON: The created tenant data or an error message.
    """
    try:
        data = request.get_json()

        if not data or 'tenant_name' not in data or 'schema_name' not in data:
            logger.warning("Missing 'tenant_name' or 'schema_name' in request data")
            raise BadRequest("The 'tenant_name' and 'schema_name' parameters are required")

        tenant_name = data['tenant_name']
        schema_name = data['schema_name']

        new_tenant = tenant_service.create_tenant(tenant_name, schema_name)

        return ApiResponse.created(data=[new_tenant.as_dict()]) 

    except BadRequest as e:
        return ApiResponse.bad_request(message=str(e))
    except Exception as e:
        logger.error(f"Error creating tenant: {e}")
        return ApiResponse.internal_server_error()


@tenant_bp.route('/tenants', methods=['GET'])
@inject
def get_all_tenants(tenant_service: TenantService):
    """
    Endpoint to retrieve all tenants.

    Returns:
        JSON: List of all tenants or an error message.
    """
    try:
        tenants = tenant_service.get_all_tenants(performed_by=request.headers.get('X-User'))

        return ApiResponse.ok(data=[tenant.as_dict() for tenant in tenants])
    except NotFound as e:
        return ApiResponse.not_found(resource='tenant', resource_id='all')
    except Exception as e:
        logger.error(f"Error fetching tenants: {e}")
        return ApiResponse.internal_server_error()


@tenant_bp.route('/tenants/<int:tenant_id>', methods=['GET'])
@inject
def get_tenant_by_id(tenant_id, tenant_service: TenantService):
    """
    Endpoint to retrieve a tenant by its ID.

    Args:
        tenant_id (int): The ID of the tenant.

    Returns:
        JSON: The tenant data or an error message.
    """
    try:
        tenant = tenant_service.get_tenant_by_id(tenant_id)

        return ApiResponse.ok(data=[tenant.as_dict()])
    except NotFound as e:
        return ApiResponse.not_found(resource='tenant', resource_id=tenant_id)
    except Exception as e:
        logger.error(f"Error fetching tenant by ID {tenant_id}: {e}")
        return ApiResponse.internal_server_error()


@tenant_bp.route('/tenants/<int:tenant_id>', methods=['PUT'])
@inject
def update_tenant(tenant_id, tenant_service: TenantService):
    """
    Endpoint to update an existing tenant by its ID.

    Body:
        JSON: Optional fields to update:
            - tenant_name (str): The new tenant name.
            - schema_name (str): The new schema name.

    Returns:
        JSON: The updated tenant data or an error message.
    """
    try:
        data = request.get_json()

        updated_tenant = tenant_service.update_tenant(
            tenant_id=tenant_id,
            tenant_name=data.get('tenant_name'),
            schema_name=data.get('schema_name'),
        )

        return ApiResponse.updated(data=[updated_tenant.as_dict()])  # Usamos ApiResponse.updated
    except BadRequest as e:
        return ApiResponse.bad_request(message=str(e))
    except NotFound as e:
        return ApiResponse.not_found(resource='tenant', resource_id=tenant_id)
    except Exception as e:
        logger.error(f"Error updating tenant with ID {tenant_id}: {e}")
        return ApiResponse.internal_server_error()


@tenant_bp.route('/tenants/<int:tenant_id>', methods=['DELETE'])
@inject
def delete_tenant(tenant_id, tenant_service: TenantService):
    """
    Endpoint to delete a tenant by its ID.

    Args:
        tenant_id (int): The ID of the tenant.

    Returns:
        JSON: A success message or an error message.
    """
    try:
        result = tenant_service.delete_tenant(tenant_id)

        if result:
            return ApiResponse.deleted(deleted_id=tenant_id)

        return ApiResponse.error(message="Tenant deletion failed.", status=400)

    except NotFound as e:
        return ApiResponse.not_found(resource='tenant', resource_id=tenant_id)
    except Exception as e:
        logger.error(f"Error deleting tenant with ID {tenant_id}: {e}")
        return ApiResponse.internal_server_error()
