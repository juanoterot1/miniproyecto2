import logging
from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.product_service import ProductService
from app.utils.api_response import ApiResponse

logger = logging.getLogger(__name__)

product_bp = Blueprint('products', __name__)

@product_bp.route('/products', methods=['POST'])
@inject
def create_product(product_service: ProductService):
    try:
        data = request.get_json()
        if not data or 'name' not in data or 'price' not in data or 'stock' not in data:
            raise BadRequest("Missing required fields: 'name', 'price', or 'stock'")

        new_product = product_service.create_product(
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            stock=data.get('stock')
        )

        return ApiResponse.created(data=[new_product.as_dict()])
    except BadRequest as e:
        return ApiResponse.bad_request(message=str(e))
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        return ApiResponse.internal_server_error()

@product_bp.route('/products', methods=['GET'])
@inject
def get_all_products(product_service: ProductService):
    try:
        products = product_service.get_all_products()
        return ApiResponse.ok(data=[product.as_dict() for product in products])
    except NotFound as e:
        return ApiResponse.not_found(resource="Products")
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        return ApiResponse.internal_server_error()

@product_bp.route('/products/<int:product_id>', methods=['GET'])
@inject
def get_product_by_id(product_id, product_service: ProductService):
    try:
        product = product_service.get_product_by_id(product_id)
        if not product:
            raise NotFound("Product not found")
        return ApiResponse.ok(data=[product.as_dict()])
    except NotFound as e:
        return ApiResponse.not_found(resource="Product", resource_id=product_id)
    except Exception as e:
        logger.error(f"Error fetching product by ID {product_id}: {e}")
        return ApiResponse.internal_server_error()

@product_bp.route('/products/<int:product_id>', methods=['PUT'])
@inject
def update_product(product_id, product_service: ProductService):
    try:
        data = request.get_json()
        updated_product = product_service.update_product(
            product_id=product_id,
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            stock=data.get('stock')
        )
        if not updated_product:
            raise NotFound("Product not found.")
        return ApiResponse.ok(data=[updated_product.as_dict()])
    except BadRequest as e:
        return ApiResponse.bad_request(message=str(e))
    except NotFound as e:
        return ApiResponse.not_found(resource="Product", resource_id=product_id)
    except Exception as e:
        logger.error(f"Error updating product with ID {product_id}: {e}")
        return ApiResponse.internal_server_error()

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
@inject
def delete_product(product_id, product_service: ProductService):
    try:
        result = product_service.delete_product(product_id)
        if not result:
            raise NotFound(f"Product with ID {product_id} not found")
        return ApiResponse.ok(data=[{"deleted_id": product_id}])
    except NotFound as e:
        return ApiResponse.not_found(resource="Product", resource_id=product_id)
    except Exception as e:
        logger.error(f"Error deleting product with ID {product_id}: {e}")
        return ApiResponse.internal_server_error()
