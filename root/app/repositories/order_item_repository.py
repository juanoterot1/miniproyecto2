from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.order_items import OrderItem

class OrderItemRepository:
    
    @staticmethod
    def create_order_item(quantity, price, id_order, id_product):
        try:
            new_order_item = OrderItem(
                quantity=quantity,
                price=price,
                id_order=id_order,
                id_product=id_product
            )
            db.session.add(new_order_item)
            db.session.commit()
            return new_order_item
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_order_item_by_id(order_item_id):
        try:
            return OrderItem.query.get(order_item_id)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def delete_order_item(order_item_id):
        try:
            order_item = OrderItem.query.get(order_item_id)
            if order_item is None:
                return None

            db.session.delete(order_item)
            db.session.commit()
            return order_item
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
