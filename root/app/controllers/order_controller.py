import logging
from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.order_service import OrderService
from app.utils.response import create_response

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
            status=data.get('status', 'pending'),
            order_items=data.get('order_items')  # Pasamos order_items para la creación
        )

        # Convertimos la orden y sus items a formato dict
        order_data = new_order.as_dict()
        order_data['order_items'] = [item.as_dict() for item in new_order.order_items]

        return create_response(success=True, result=order_data, status=201)

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return create_response(success=False, message=str(e), status=400)
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        return create_response(success=False, message="Internal server error", status=500)

@order_bp.route('/orders/<int:order_id>', methods=['GET'])
@inject
def get_order_by_id(order_id, order_service: OrderService):
    try:
        order = order_service.get_order_by_id(order_id)
        if not order:
            raise NotFound("Order not found")

        # Incluir order_items en la respuesta
        order_data = order.as_dict()
        order_data['order_items'] = [item.as_dict() for item in order.order_items]

        return create_response(success=True, result=order_data, status=200)

    except NotFound as e:
        return create_response(success=False, message=str(e), status=404)
    except Exception as e:
        logger.error(f"Error fetching order by ID {order_id}: {e}")
        return create_response(success=False, message="Internal server error", status=500)

@order_bp.route('/orders', methods=['GET'])
@inject
def get_all_orders_paginated(order_service: OrderService):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        filters = {
            "status": request.args.get('status'),
            "id_customer": request.args.get('id_customer', type=int)
        }

        orders, total = order_service.get_orders_paginated(page, per_page, **filters)

        # Incluir order_items en cada orden
        orders_data = [{
            **order.as_dict(),
            "order_items": [item.as_dict() for item in order.order_items]
        } for order in orders]

        return create_response(success=True, result={"data": orders_data, "total": total}, status=200)

    except BadRequest as e:
        logger.warning(f"Bad request: {e}")
        return create_response(success=False, message=str(e), status=400)
    except Exception as e:
        logger.error(f"Error fetching paginated orders: {e}")
        return create_response(success=False, message="Internal server error", status=500)


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
        return create_response(success=True, result=updated_order.as_dict(), status=200)

    except BadRequest as e:
        return create_response(success=False, message=str(e), status=400)
    except NotFound as e:
        return create_response(success=False, message=str(e), status=404)
    except Exception as e:
        logger.error(f"Error updating order with ID {order_id}: {e}")
        return create_response(success=False, message="Internal server error", status=500)

@order_bp.route('/orders/<int:order_id>', methods=['DELETE'])
@inject
def delete_order(order_id, order_service: OrderService):
    try:
        result = order_service.delete_order(order_id)
        if not result:
            raise NotFound("Order not found")

        return create_response(success=True, result={"deleted_id": order_id}, status=200)

    except NotFound as e:
        return create_response(success=False, message=str(e), status=404)
    except Exception as e:
        logger.error(f"Error deleting order with ID {order_id}: {e}")
        return create_response(success=False, message="Internal server error", status=500)
