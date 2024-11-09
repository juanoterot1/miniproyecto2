from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.inventory import Inventory

class InventoryRepository:
    
    @staticmethod
    def create_inventory_item(product_id, stock_quantity, restock_date=None):
        try:
            new_item = Inventory(
                product_id=product_id,
                stock_quantity=stock_quantity,
                restock_date=restock_date
            )
            db.session.add(new_item)
            db.session.commit()
            return new_item
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_inventory_item_by_id(item_id):
        try:
            return Inventory.query.get(item_id)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_inventory_items_paginated(page, per_page, product_id=None, min_stock=None, max_stock=None):
        query = Inventory.query
        if product_id:
            query = query.filter_by(product_id=product_id)
        if min_stock is not None:
            query = query.filter(Inventory.stock_quantity >= min_stock)
        if max_stock is not None:
            query = query.filter(Inventory.stock_quantity <= max_stock)

        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        return paginated.items, paginated.total

    @staticmethod
    def delete_inventory_item(item_id):
        try:
            item = Inventory.query.get(item_id)
            if item is None:
                return None

            db.session.delete(item)
            db.session.commit()
            return item
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
