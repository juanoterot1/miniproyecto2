from app.models.tenants import Tenant
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db

class TenantRepository:

    def __init__(self):
        pass

    def create_tenant(self, tenant_name, schema_name):
        """
        Registers a new tenant in the public schema.

        Args:
            tenant_name (str): The name of the tenant.
            schema_name (str): The schema name of the tenant.

        Returns:
            Tenant: The newly created tenant object.
        """
        tenant = Tenant(tenant_name=tenant_name, schema_name=schema_name)
        db.session.add(tenant)  # Usa db.session aquí
        db.session.commit()
        return tenant

    def get_tenant_by_schema(self, schema_name):
        """
        Retrieves a tenant by its schema name.

        Args:
            schema_name (str): The schema name of the tenant.

        Returns:
            Tenant: The tenant object if found, otherwise None.
        """
        return db.session.query(Tenant).filter_by(schema_name=schema_name).first()  # Cambia self.db_session a db.session

    def get_all_tenants(self):
        """
        Retrieves all tenants.

        Returns:
            list: A list of all tenants.
        """
        return db.session.query(Tenant).all()  # Cambia self.db_session a db.session

    def get_tenant_by_id(self, tenant_id):
        """
        Retrieves a tenant by its ID.

        Args:
            tenant_id (int): The ID of the tenant.

        Returns:
            Tenant: The tenant object if found, otherwise None.
        """
        return db.session.query(Tenant).filter_by(tenant_id=tenant_id).first()  # Cambia self.db_session a db.session

    def update_tenant(self, tenant_id, tenant_name=None, schema_name=None):
        """
        Updates an existing tenant.

        Args:
            tenant_id (int): The ID of the tenant to update.
            tenant_name (str): The new name of the tenant (optional).
            schema_name (str): The new schema name of the tenant (optional).

        Returns:
            Tenant: The updated tenant object.
        """
        try:
            tenant = db.session.query(Tenant).get(tenant_id)  # Cambia self.db_session a db.session
            if tenant is None:
                return None
            
            if tenant_name:
                tenant.tenant_name = tenant_name
            if schema_name:
                tenant.schema_name = schema_name
            
            db.session.commit()  # Cambia self.db_session a db.session
            return tenant
        except SQLAlchemyError as e:
            db.session.rollback()  # Cambia self.db_session a db.session
            raise e

    def delete_tenant(self, tenant_id):
        """
        Deletes a tenant by its ID.

        Args:
            tenant_id (int): The ID of the tenant.

        Returns:
            Tenant: The deleted tenant object.
        """
        try:
            tenant = db.session.query(Tenant).get(tenant_id)  # Cambia self.db_session a db.session
            if tenant is None:
                return None
            
            db.session.delete(tenant)  # Cambia self.db_session a db.session
            db.session.commit()  # Cambia self.db_session a db.session
            return tenant
        except SQLAlchemyError as e:
            db.session.rollback()  # Cambia self.db_session a db.session
            raise e
