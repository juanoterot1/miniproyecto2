import logging
from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.sale_service import SaleService
from app.utils.response import create_response

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

        return create_response(success=True, result=new_sale.as_dict(), status=201)
    except BadRequest as e:
        return create_response(success=False, message=str(e), status=400)
    except Exception as e:
        logger.error(f"Error creating sale: {e}")
        return create_response(success=False, message="Internal server error", status=500)

@sale_bp.route('/sales', methods=['GET'])
@inject
def get_sales_paginated(sale_service: SaleService):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        sales, total = sale_service.get_sales_paginated(page, per_page)
        return create_response(success=True, result={"data": [sale.as_dict() for sale in sales], "total": total}, status=200)
    except Exception as e:
        logger.error(f"Error fetching paginated sales: {e}")
        return create_response(success=False, message="Internal server error", status=500)

@sale_bp.route('/sales/<int:sale_id>', methods=['GET'])
@inject
def get_sale_by_id(sale_id, sale_service: SaleService):
    try:
        sale = sale_service.get_sale_by_id(sale_id)
        if not sale:
            raise NotFound("Sale not found")
        return create_response(success=True, result=sale.as_dict(), status=200)
    except NotFound as e:
        return create_response(success=False, message=str(e), status=404)
    except Exception as e:
        logger.error(f"Error fetching sale by ID {sale_id}: {e}")
        return create_response(success=False, message="Internal server error", status=500)

@sale_bp.route('/sales/<int:sale_id>', methods=['DELETE'])
@inject
def delete_sale(sale_id, sale_service: SaleService):
    try:
        result = sale_service.delete_sale(sale_id)
        if not result:
            raise NotFound(f"Sale with ID {sale_id} not found")
        return create_response(success=True, result={"deleted_id": sale_id}, status=200)
    except NotFound as e:
        return create_response(success=False, message=str(e), status=404)
    except Exception as e:
        logger.error(f"Error deleting sale with ID {sale_id}: {e}")
        return create_response(success=False, message="Internal server error", status=500)
