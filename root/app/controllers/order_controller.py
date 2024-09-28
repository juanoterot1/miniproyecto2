import logging
from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.order_service import OrderService
from app.utils.api_response import ApiResponse

logger = logging.getLogger(__name__)

order_bp = Blueprint('orders', __name__)

@order_bp.route('/orders', methods=['POST'])
@inject
def create_order(order_service: OrderService):
    try:
        data = request.get_json()
        if not data or 'payment_method' not in data or 'id_customer' not in data:
            raise BadRequest("Missing required fields: 'payment_method' and 'id_customer'")

        new_order = order_service.create_order(
            payment_method=data.get('payment_method'),
            id_customer=data.get('id_customer'),
            delivery_date=data.get('delivery_date'),
            status=data.get('status', 'pending')
        )

        return ApiResponse.created(data=[new_order.as_dict()])
    except BadRequest as e:
        return ApiResponse.bad_request(message=str(e))
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        return ApiResponse.internal_server_error()

@order_bp.route('/orders', methods=['GET'])
@inject
def get_all_orders(order_service: OrderService):
    try:
        orders = order_service.get_all_orders()
        return ApiResponse.ok(data=[order.as_dict() for order in orders])
    except NotFound as e:
        return ApiResponse.not_found(resource="Orders")
    except Exception as e:
        logger.error(f"Error fetching orders: {e}")
        return ApiResponse.internal_server_error()

@order_bp.route('/orders/<int:order_id>', methods=['GET'])
@inject
def get_order_by_id(order_id, order_service: OrderService):
    try:
        order = order_service.get_order_by_id(order_id)
        if not order:
            raise NotFound("Order not found")
        return ApiResponse.ok(data=[order.as_dict()])
    except NotFound as e:
        return ApiResponse.not_found(resource="Order", resource_id=order_id)
    except Exception as e:
        logger.error(f"Error fetching order by ID {order_id}: {e}")
        return ApiResponse.internal_server_error()

@order_bp.route('/orders/<int:order_id>', methods=['PUT'])
@inject
def update_order(order_id, order_service: OrderService):
    try:
        data = request.get_json()
        updated_order = order_service.update_order(
            order_id=order_id,
            payment_method=data.get('payment_method'),
            status=data.get('status'),
            delivery_date=data.get('delivery_date')
        )
        if not updated_order:
            raise NotFound("Order not found.")
        return ApiResponse.ok(data=[updated_order.as_dict()])
    except BadRequest as e:
        return ApiResponse.bad_request(message=str(e))
    except NotFound as e:
        return ApiResponse.not_found(resource="Order", resource_id=order_id)
    except Exception as e:
        logger.error(f"Error updating order with ID {order_id}: {e}")
        return ApiResponse.internal_server_error()

@order_bp.route('/orders/<int:order_id>', methods=['DELETE'])
@inject
def delete_order(order_id, order_service: OrderService):
    try:
        result = order_service.delete_order(order_id)
        if not result:
            raise NotFound(f"Order with ID {order_id} not found")
        return ApiResponse.ok(data=[{"deleted_id": order_id}])
    except NotFound as e:
        return ApiResponse.not_found(resource="Order", resource_id=order_id)
    except Exception as e:
        logger.error(f"Error deleting order with ID {order_id}: {e}")
        return ApiResponse.internal_server_error()
