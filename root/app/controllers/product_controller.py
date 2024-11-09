import logging
from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.product_service import ProductService
from app.utils.response import create_response

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

        return create_response(success=True, result=new_product.as_dict(), status=201)
    except BadRequest as e:
        return create_response(success=False, message=str(e), status=400)
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        return create_response(success=False, message="Internal server error", status=500)

@product_bp.route('/products', methods=['GET'])
@inject
def get_products_paginated(product_service: ProductService):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        products, total = product_service.get_products_paginated(page, per_page)
        return create_response(success=True, result={"data": [product.as_dict() for product in products], "total": total}, status=200)
    except Exception as e:
        logger.error(f"Error fetching paginated products: {e}")
        return create_response(success=False, message="Internal server error", status=500)

@product_bp.route('/products/<int:product_id>', methods=['GET'])
@inject
def get_product_by_id(product_id, product_service: ProductService):
    try:
        product = product_service.get_product_by_id(product_id)
        if not product:
            raise NotFound("Product not found")
        return create_response(success=True, result=product.as_dict(), status=200)
    except NotFound as e:
        return create_response(success=False, message=str(e), status=404)
    except Exception as e:
        logger.error(f"Error fetching product by ID {product_id}: {e}")
        return create_response(success=False, message="Internal server error", status=500)

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
        return create_response(success=True, result=updated_product.as_dict(), status=200)
    except BadRequest as e:
        return create_response(success=False, message=str(e), status=400)
    except NotFound as e:
        return create_response(success=False, message=str(e), status=404)
    except Exception as e:
        logger.error(f"Error updating product with ID {product_id}: {e}")
        return create_response(success=False, message="Internal server error", status=500)

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
@inject
def delete_product(product_id, product_service: ProductService):
    try:
        result = product_service.delete_product(product_id)
        if not result:
            raise NotFound(f"Product with ID {product_id} not found")
        return create_response(success=True, result={"deleted_id": product_id}, status=200)
    except NotFound as e:
        return create_response(success=False, message=str(e), status=404)
    except Exception as e:
        logger.error(f"Error deleting product with ID {product_id}: {e}")
        return create_response(success=False, message="Internal server error", status=500)
