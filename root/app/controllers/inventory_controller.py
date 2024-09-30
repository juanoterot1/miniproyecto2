import logging
from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.inventory_service import InventoryService
from app.utils.api_response import ApiResponse

logger = logging.getLogger(__name__)

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/inventory', methods=['POST'])
@inject
def create_inventory_item(inventory_service: InventoryService):
    try:
        data = request.get_json()
        if not data or 'product_id' not in data or 'stock_quantity' not in data:
            raise BadRequest("Missing required fields: 'product_id' and 'stock_quantity'")

        new_inventory_item = inventory_service.create_inventory_item(
            product_id=data.get('product_id'),
            stock_quantity=data.get('stock_quantity'),
            restock_date=data.get('restock_date')
        )

        return ApiResponse.created(data=[new_inventory_item.as_dict()])
    except BadRequest as e:
        return ApiResponse.bad_request(message=str(e))
    except Exception as e:
        logger.error(f"Error creating inventory item: {e}")
        return ApiResponse.internal_server_error()

@inventory_bp.route('/inventory/<int:item_id>', methods=['GET'])
@inject
def get_inventory_item_by_id(item_id, inventory_service: InventoryService):
    try:
        item = inventory_service.get_inventory_item_by_id(item_id)
        if not item:
            raise NotFound("Inventory Item not found")
        return ApiResponse.ok(data=[item.as_dict()])
    except NotFound as e:
        return ApiResponse.not_found(resource="Inventory Item", resource_id=item_id)
    except Exception as e:
        logger.error(f"Error fetching inventory item by ID {item_id}: {e}")
        return ApiResponse.internal_server_error()
