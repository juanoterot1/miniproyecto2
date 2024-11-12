from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.products import Product

class ProductRepository:
    
    @staticmethod
    def create_product(name, description=None, price=0.0, stock=0):
        try:
            new_product = Product(
                name=name,
                description=description,
                price=price,
                stock=stock
            )
            db.session.add(new_product)
            db.session.commit()
            return new_product
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_products_paginated(page, per_page):
        try:
            # Orden descendente por id para mostrar los productos más recientes primero
            paginated = Product.query.order_by(Product.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
            return paginated.items, paginated.total
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_product_by_id(product_id):
        try:
            return Product.query.get(product_id)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def update_product(product_id, name=None, description=None, price=None, stock=None):
        try:
            product = Product.query.get(product_id)
            if product is None:
                return None

            if name:
                product.name = name
            if description:
                product.description = description
            if price is not None:
                product.price = price
            if stock is not None:
                product.stock = stock

            db.session.commit()
            return product
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_product(product_id):
        try:
            product = Product.query.get(product_id)
            if product is None:
                return None

            db.session.delete(product)
            db.session.commit()
            return product
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
