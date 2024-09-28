from app.extensions import db
from flask_injector import inject
from sqlalchemy import text
from sqlalchemy.schema import CreateSchema
from werkzeug.exceptions import InternalServerError, NotFound, BadRequest
from app.repositories.tenants_repository import TenantRepository
from app.services.usage_log_service import UsageLogService

class TenantService:

    @inject
    def __init__(self, tenant_repository: TenantRepository, usage_log_service: UsageLogService):
        self.tenant_repository = tenant_repository
        self.usage_log_service = usage_log_service

    def create_tenant(self, tenant_name, schema_name):
        """
        Creates a new tenant and a schema in the database, then runs the DDL SQL to initialize the schema.
        """
        try:
            # Set session to Public Schema
            self._set_search_path('public')
            print(f"Creating a new tenant: {tenant_name} with schema: {schema_name}")

            if not tenant_name or not schema_name:
                print("The 'tenant_name' and 'schema_name' parameters are required")
                raise BadRequest("The 'tenant_name' and 'schema_name' parameters are required")

            # Verify if the schema exists
            existing_tenant = self.tenant_repository.get_tenant_by_schema(schema_name)
            if existing_tenant:
                print(f"Schema {schema_name} already exists for another tenant.")
                raise BadRequest(f"Schema {schema_name} already exists.")

            # Create new Schema
            self._create_schema(schema_name)

            # Return Session to Public Schema
            self._set_search_path('public')
            new_tenant = self.tenant_repository.create_tenant(tenant_name, schema_name)

            if not new_tenant:
                raise InternalServerError("An error occurred while creating the tenant in the public schema.")
            
            # Execute DDL into new SCHEMA
            self._execute_ddl_for_schema(schema_name)

            self._set_search_path('public')

            return new_tenant
        except BadRequest as e:
            print(f"Bad request: {e}")
            raise
        except Exception as e:
            print(f"Error creating tenant: {e}")
            raise InternalServerError("An internal error occurred while creating the tenant.")

    def _create_schema(self, schema_name):
        """Creates a new schema in the database."""
        try:
            print(f"Creating schema: {schema_name}")
            db.session.execute(CreateSchema(schema_name))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error creating schema {schema_name}: {e}")
            raise InternalServerError(f"An error occurred while creating the schema {schema_name}.")

    def _set_search_path(self, schema_name):
        """Sets the search_path to the given schema."""
        try:
            print(f"Setting search_path to {schema_name}")
            db.session.execute(text(f"SET search_path TO {schema_name}"))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error setting search_path to {schema_name}: {e}")
            raise InternalServerError(f"An error occurred while setting search_path to {schema_name}.")

    def _execute_ddl_for_schema(self, schema_name):
        """
        Executes the SQL DDL script to create the necessary tables in the new schema.
        """
        try:
            ddl_path = 'db/assets/ddl.sql'
            print(f"Executing DDL script from: {ddl_path}")

            with open(ddl_path, 'r') as ddl_file:
                ddl_sql = ddl_file.read()

            print(ddl_sql)

            with db.session.begin():
                self._set_search_path(schema_name)
                print("Executing DDL SQL")
                db.session.execute(text(ddl_sql))

            print(f"DDL executed successfully for schema: {schema_name}")
        except Exception as e:
            print(f"Error executing DDL for schema {schema_name}: {e}")
            db.session.rollback()
            raise InternalServerError(f"An error occurred while executing DDL for schema {schema_name}.")

    def get_all_tenants(self):
        """Retrieves all tenants, always from the 'public' schema."""
        try:
            self._set_search_path('public')
            print("Fetching all tenants")
            tenants = self.tenant_repository.get_all_tenants()

            if not tenants:
                print("No tenants found.")
                raise NotFound("No tenants found.")

            return tenants
        except Exception as e:
            print(f"Error fetching tenants: {e}")
            raise InternalServerError("An internal error occurred while fetching tenants.")

    def get_tenant_by_id(self, tenant_id):
        """Fetches a tenant by ID from the 'public' schema."""
        try:
            self._set_search_path('public')
            print(f"Fetching tenant with ID: {tenant_id}")
            tenant = self.tenant_repository.get_tenant_by_id(tenant_id)

            if not tenant:
                print(f"Tenant with ID {tenant_id} not found.")
                raise NotFound("Tenant not found.")

            return tenant
        except NotFound as e:
            print(f"Not found: {e}")
            raise
        except Exception as e:
            print(f"Error fetching tenant by ID {tenant_id}: {e}")
            raise InternalServerError("An internal error occurred while fetching the tenant.")

    def update_tenant(self, tenant_id, tenant_name=None, schema_name=None):
        """Updates an existing tenant in the 'public' schema."""
        try:
            self._set_search_path('public')
            print(f"Updating tenant with ID: {tenant_id}")
            updated_tenant = self.tenant_repository.update_tenant(tenant_id, tenant_name, schema_name)

            if not updated_tenant:
                print(f"Tenant with ID {tenant_id} not found.")
                raise NotFound("Tenant not found.")
            
            return updated_tenant
        except NotFound as e:
            print(f"Not found: {e}")
            raise
        except Exception as e:
            print(f"Error updating tenant with ID {tenant_id}: {e}")
            raise InternalServerError("An internal error occurred while updating the tenant.")

    def delete_tenant(self, tenant_id):
        """Deletes a tenant by its ID, operating in the 'public' schema."""
        try:
            self._set_search_path('public')
            print(f"Deleting tenant with ID: {tenant_id}")
            result = self.tenant_repository.delete_tenant(tenant_id)

            if not result:
                print(f"Tenant with ID {tenant_id} not found.")
                raise NotFound(f"Tenant with ID {tenant_id} not found.")
            
            return result
        except Exception as e:
            print(f"Error deleting tenant with ID {tenant_id}: {e}")
            raise InternalServerError("An internal error occurred while deleting the tenant.")
