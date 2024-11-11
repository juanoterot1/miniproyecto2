import logging
from flask_injector import inject
from werkzeug.exceptions import InternalServerError, NotFound
from sqlalchemy import func
from app.extensions import db
from app.repositories.order_repository import OrderRepository
from app.services.order_item_service import OrderItemService
from app.models.orders import Order
from app.models.order_items import OrderItem
from app.models.customers import Customer
from app.models.products import Product


logger = logging.getLogger(__name__)

class OrderService:

    @inject
    def __init__(self, order_repository: OrderRepository, order_item_service: OrderItemService):
        self.order_repository = order_repository
        self.order_item_service = order_item_service

    def create_order(self, payment_method, id_customer, delivery_date=None, status='pending', order_items=None):
        try:
            logger.info(f"Creating new order for customer ID: {id_customer}")
            new_order = self.order_repository.create_order(
                payment_method, id_customer, delivery_date, status
            )

            if order_items:
                for item in order_items:
                    self.order_item_service.create_order_item(
                        quantity=item['quantity'],
                        price=item['price'],
                        id_order=new_order.id,
                        id_product=item['id_product']
                    )

            return new_order
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            raise InternalServerError("An error occurred while creating the order.")

    def get_orders_paginated(self, page, per_page, **filters):
        try:
            logger.info(f"Fetching orders with pagination: page {page}, per_page {per_page}")
            orders, total = self.order_repository.get_orders_paginated(page, per_page, **filters)
            return orders, total
        except Exception as e:
            logger.error(f"Error fetching paginated orders: {e}")
            raise InternalServerError("An error occurred while fetching orders.")

    def get_order_by_id(self, order_id):
        try:
            order = self.order_repository.get_order_by_id(order_id)
            if not order:
                raise NotFound("Order not found")
            return order
        except Exception as e:
            logger.error(f"Error retrieving order by ID {order_id}: {e}")
            raise InternalServerError("An error occurred while retrieving the order.")

    def update_order(self, order_id, payment_method=None, delivery_date=None, status=None):
        try:
            updated_order = self.order_repository.update_order(
                order_id, payment_method, delivery_date, status
            )
            if not updated_order:
                raise NotFound("Order not found")
            return updated_order
        except Exception as e:
            logger.error(f"Error updating order: {e}")
            raise InternalServerError("An error occurred while updating the order.")

    def delete_order(self, order_id):
        try:
            result = self.order_repository.delete_order(order_id)
            if not result:
                raise NotFound("Order not found")
            return result
        except Exception as e:
            logger.error(f"Error deleting order: {e}")
            raise InternalServerError("An error occurred while deleting the order.")

    def get_statistics(self):
        return {
            "total_orders": self.order_repository.get_total_orders(),
            "total_completed_orders": self.order_repository.get_total_completed_orders(),
            "total_pending_orders": self.order_repository.get_total_pending_orders(),
        }

    def get_top_customers(self, limit=3):
        results = (
            db.session.query(
                Customer.id,
                Customer.full_name,
                func.count(Order.id).label('completed_order_count')
            )
            .join(Order, Customer.id == Order.id_customer)  # Unión con la tabla de órdenes
            .filter(Order.status == 'Completada')  # Solo órdenes completadas
            .group_by(Customer.id)
            .order_by(func.count(Order.id).desc())  # Orden descendente por cantidad de órdenes
            .limit(limit)
        )

        top_customers = [
            {
                "customer_id": row.id,
                "customer_name": row.full_name,
                "completed_order_count": row.completed_order_count
            }
            for row in results
        ]
        return top_customers

    def get_top_selling_products(self, limit=3):
        try:
            results = (
                db.session.query(
                    Product.id,
                    Product.name,
                    func.sum(OrderItem.quantity).label('total_quantity_sold')
                )
                .join(OrderItem, Product.id == OrderItem.id_product)  # Unir con la tabla OrderItem
                .join(Order, Order.id == OrderItem.id_order)  # Unir con la tabla Order para filtrar por estado
                .filter(Order.status == 'Completada')  # Solo considerar órdenes completadas
                .group_by(Product.id)
                .order_by(func.sum(OrderItem.quantity).desc())  # Ordenar por la cantidad vendida en orden descendente
                .limit(limit)
            )

            top_products = [
                {
                    "product_id": row.id,
                    "product_name": row.name,
                    "total_quantity_sold": row.total_quantity_sold
                }
                for row in results
            ]
            return top_products

        except Exception as e:
            logger.error(f"Error fetching top selling products: {e}")
            raise InternalServerError("An error occurred while fetching top selling products.")
