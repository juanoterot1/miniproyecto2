from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.customers import Customer

class CustomerRepository:
    
    @staticmethod
    def create_customer(full_name, email, phone, address=None, credit_limit=0.0, created_at=None):
        """Creates a new customer."""
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
    def get_all_customers():
        """Retrieves all customers."""
        try:
            return Customer.query.all()
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_customer_by_id(customer_id):
        """Retrieves a customer by its ID."""
        try:
            return Customer.query.get(customer_id)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_customer_by_email(email):
        """Retrieves a customer by email."""
        try:
            return Customer.query.filter_by(email=email).first()
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def update_customer(customer_id, full_name=None, email=None, phone=None, address=None, credit_limit=None):
        """Updates an existing customer."""
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
        """Deletes a customer by its ID."""
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