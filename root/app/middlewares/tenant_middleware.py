from flask import g, request, abort
from sqlalchemy import text
from app.models.tenants import Tenant
from app.extensions import db

EXCLUDED_PREFIXES = ['/api/v1/tenants']

def tenant_middleware():
    """
    Middleware to set the tenant schema for the current request, excluding routes that start with certain prefixes.
    """
    # Check if the requested route starts with an excluded prefix
    if any(request.path.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
        return  # Skip middleware logic for excluded routes

    tenant_name = request.headers.get('X-Tenant')

    if not tenant_name:
        abort(400, description="Tenant name is required in the X-Tenant header")

    # Perform tenant lookup in the "public" schema first
    try:
        # Ensure the search_path is set to 'public' to query the 'tenants' table
        query_public_schema = text('SET search_path TO public')
        db.session.execute(query_public_schema)

        # Look for the tenant in the 'tenants' table within the public schema
        tenant = Tenant.query.filter_by(schema_name=tenant_name).first()
    except Exception as e:
        abort(500, description=f"Error querying tenant information: {str(e)}")

    if not tenant:
        abort(404, description=f"Tenant {tenant_name} not found")

    schema_name = tenant.schema_name

    try:
        # Set the search_path to the tenant schema and 'public'
        query_set_schema = text(f'SET search_path TO {schema_name}, public')
        db.session.execute(query_set_schema)
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"Error setting search path for tenant schema: {str(e)}")

    # Store the current tenant in the request context (optional)
    g.current_tenant = tenant
