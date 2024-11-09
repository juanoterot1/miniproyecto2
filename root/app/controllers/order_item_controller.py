import logging
from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.order_item_service import OrderItemService
from app.utils.response import create_response

logger = logging.getLogger(__name__)

order_item_bp = Blueprint('order_items', __name__)

@order_item_bp.route('/order_items', methods=['POST'])
@inject
def create_order_item(order_item_service: OrderItemService):
    try:
        data = request.get_json()
        if not data or 'quantity' not in data or 'price' not in data or 'id_order' not in data or 'id_product' not in data:
            raise BadRequest("Missing required fields: 'quantity', 'price', 'id_order', 'id_product'")

        new_order_item = order_item_service.create_order_item(
            quantity=data.get('quantity'),
            price=data.get('price'),
            id_order=data.get('id_order'),
            id_product=data.get('id_product')
        )

        return create_response(success=True, result=new_order_item.as_dict(), status=201)
    except BadRequest as e:
        return create_response(success=False, message=str(e), status=400)
    except Exception as e:
        logger.error(f"Error creating order item: {e}")
        return create_response(success=False, message="Internal server error", status=500)

@order_item_bp.route('/order_items', methods=['GET'])
@inject
def get_order_items_paginated(order_item_service: OrderItemService):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        id_order = request.args.get('id_order', type=int)

        items, total = order_item_service.get_order_items_paginated(page, per_page, id_order=id_order)

        return create_response(success=True, result={"data": [item.as_dict() for item in items], "total": total}, status=200)

    except BadRequest as e:
        return create_response(success=False, message=str(e), status=400)
    except Exception as e:
        logger.error(f"Error fetching paginated order items: {e}")
        return create_response(success=False, message="Internal server error", status=500)

@order_item_bp.route('/order_items/<int:order_item_id>', methods=['GET'])
@inject
def get_order_item_by_id(order_item_id, order_item_service: OrderItemService):
    try:
        order_item = order_item_service.get_order_item_by_id(order_item_id)
        if not order_item:
            raise NotFound("Order Item not found")
        return create_response(success=True, result=order_item.as_dict(), status=200)
    except NotFound as e:
        return create_response(success=False, message=str(e), status=404)
    except Exception as e:
        logger.error(f"Error fetching order item by ID {order_item_id}: {e}")
        return create_response(success=False, message="Internal server error", status=500)

@order_item_bp.route('/order_items/<int:order_item_id>', methods=['DELETE'])
@inject
def delete_order_item(order_item_id, order_item_service: OrderItemService):
    try:
        result = order_item_service.delete_order_item(order_item_id)
        if not result:
            raise NotFound(f"Order Item with ID {order_item_id} not found")
        return create_response(success=True, result={"deleted_id": order_item_id}, status=200)
    except NotFound as e:
        return create_response(success=False, message=str(e), status=404)
    except Exception as e:
        logger.error(f"Error deleting order item with ID {order_item_id}: {e}")
        return create_response(success=False, message="Internal server error", status=500)
