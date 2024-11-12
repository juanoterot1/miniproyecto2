from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.customers import Customer

class CustomerRepository:
    
    @staticmethod
    def create_customer(full_name, email, phone, address=None, credit_limit=0.0, created_at=None):
        try:
            new_customer = Customer(
                full_name=full_name,
                email=email,
                phone=phone,
                address=address,
                credit_limit=credit_limit,
                created_at=created_at
            )
            db.session.add(new_customer)
            db.session.commit()
            return new_customer
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
        
    @staticmethod
    def get_customers_paginated(page, per_page, full_name=None, email=None):
        query = Customer.query
        if full_name:
            query = query.filter(Customer.full_name.ilike(f"%{full_name}%"))
        if email:
            query = query.filter(Customer.email.ilike(f"%{email}%"))
        
        # Orden descendente por id para mostrar los clientes más recientes primero
        query = query.order_by(Customer.id.desc())

        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        return paginated.items, paginated.total

    @staticmethod
    def get_customer_by_id(customer_id):
        try:
            return Customer.query.get(customer_id)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def update_customer(customer_id, full_name=None, email=None, phone=None, address=None, credit_limit=None):
        try:
            customer = Customer.query.get(customer_id)
            if customer is None:
                return None

            if full_name:
                customer.full_name = full_name
            if email:
                customer.email = email
            if phone:
                customer.phone = phone
            if address:
                customer.address = address
            if credit_limit is not None:
                customer.credit_limit = credit_limit

            db.session.commit()
            return customer
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_customer(customer_id):
        try:
            customer = Customer.query.get(customer_id)
            if customer is None:
                return None

            db.session.delete(customer)
            db.session.commit()
            return customer
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
