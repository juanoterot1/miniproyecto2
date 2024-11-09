import logging
from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.inventory_service import InventoryService
from app.utils.response import create_response

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

        return create_response(success=True, result=new_inventory_item.as_dict(), status=201)

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return create_response(success=False, message=str(e), status=400)
    except Exception as e:
        logger.error(f"Error creating inventory item: {e}")
        return create_response(success=False, message="Internal server error", status=500)

@inventory_bp.route('/inventory/<int:item_id>', methods=['GET'])
@inject
def get_inventory_item_by_id(item_id, inventory_service: InventoryService):
    try:
        item = inventory_service.get_inventory_item_by_id(item_id)
        if not item:
            raise NotFound("Inventory Item not found")
        return create_response(success=True, result=item.as_dict(), status=200)
    except NotFound as e:
        return create_response(success=False, message=str(e), status=404)
    except Exception as e:
        logger.error(f"Error fetching inventory item by ID {item_id}: {e}")
        return create_response(success=False, message="Internal server error", status=500)

@inventory_bp.route('/inventory', methods=['GET'])
@inject
def get_inventory_items_paginated(inventory_service: InventoryService):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        filters = {
            "product_id": request.args.get('product_id', type=int),
            "min_stock": request.args.get('min_stock', type=int),
            "max_stock": request.args.get('max_stock', type=int)
        }

        items, total = inventory_service.get_inventory_items_paginated(page, per_page, **filters)

        return create_response(success=True, result={"data": [item.as_dict() for item in items], "total": total}, status=200)

    except BadRequest as e:
        logger.warning(f"Bad request: {e}")
        return create_response(success=False, message=str(e), status=400)

    except Exception as e:
        logger.error(f"Error fetching paginated inventory items: {e}")
        return create_response(success=False, message="Internal server error", status=500)

@inventory_bp.route('/inventory/<int:item_id>', methods=['DELETE'])
@inject
def delete_inventory_item(item_id, inventory_service: InventoryService):
    try:
        result = inventory_service.delete_inventory_item(item_id)

        if not result:
            raise NotFound("Inventory item not found")

        return create_response(success=True, result={"deleted_id": item_id}, status=200)

    except NotFound as e:
        logger.error(f"Inventory item not found: {e}")
        return create_response(success=False, message=str(e), status=404)

    except Exception as e:
        logger.error(f"Error deleting inventory item with ID {item_id}: {e}")
        return create_response(success=False, message="Internal server error", status=500)
