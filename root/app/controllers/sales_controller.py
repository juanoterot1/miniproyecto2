import logging
from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.sale_service import SaleService
from app.utils.api_response import ApiResponse

logger = logging.getLogger(__name__)

sale_bp = Blueprint('sales', __name__)

@sale_bp.route('/sales', methods=['POST'])
@inject
def create_sale(sale_service: SaleService):
    try:
        data = request.get_json()
        if not data or 'total_amount' not in data or 'id_customer' not in data:
            raise BadRequest("Missing required fields: 'total_amount' and 'id_customer'")

        new_sale = sale_service.create_sale(
            total_amount=data.get('total_amount'),
            id_customer=data.get('id_customer'),
            id_order=data.get('id_order')
        )

        return ApiResponse.created(data=[new_sale.as_dict()])
    except BadRequest as e:
        return ApiResponse.bad_request(message=str(e))
    except Exception as e:
        logger.error(f"Error creating sale: {e}")
        return ApiResponse.internal_server_error()

@sale_bp.route('/sales/<int:sale_id>', methods=['GET'])
@inject
def get_sale_by_id(sale_id, sale_service: SaleService):
    try:
        sale = sale_service.get_sale_by_id(sale_id)
        if not sale:
            raise NotFound("Sale not found")
        return ApiResponse.ok(data=[sale.as_dict()])
    except NotFound as e:
        return ApiResponse.not_found(resource="Sale", resource_id=sale_id)
    except Exception as e:
        logger.error(f"Error fetching sale by ID {sale_id}: {e}")
        return ApiResponse.internal_server_error()
