import logging
from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.order_item_service import OrderItemService
from app.utils.api_response import ApiResponse

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

        return ApiResponse.created(data=[new_order_item.as_dict()])
    except BadRequest as e:
        return ApiResponse.bad_request(message=str(e))
    except Exception as e:
        logger.error(f"Error creating order item: {e}")
        return ApiResponse.internal_server_error()

@order_item_bp.route('/order_items/<int:order_item_id>', methods=['GET'])
@inject
def get_order_item_by_id(order_item_id, order_item_service: OrderItemService):
    try:
        order_item = order_item_service.get_order_item_by_id(order_item_id)
        if not order_item:
            raise NotFound("Order Item not found")
        return ApiResponse.ok(data=[order_item.as_dict()])
    except NotFound as e:
        return ApiResponse.not_found(resource="Order Item", resource_id=order_item_id)
    except Exception as e:
        logger.error(f"Error fetching order item by ID {order_item_id}: {e}")
        return ApiResponse.internal_server_error()

@order_item_bp.route('/order_items/<int:order_item_id>', methods=['DELETE'])
@inject
def delete_order_item(order_item_id, order_item_service: OrderItemService):
    try:
        result = order_item_service.delete_order_item(order_item_id)
        if not result:
            raise NotFound(f"Order Item with ID {order_item_id} not found")
        return ApiResponse.ok(data=[{"deleted_id": order_item_id}])
    except NotFound as e:
        return ApiResponse.not_found(resource="Order Item", resource_id=order_item_id)
    except Exception as e:
        logger.error(f"Error deleting order item with ID {order_item_id}: {e}")
        return ApiResponse.internal_server_error()
