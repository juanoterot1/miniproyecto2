from datetime import datetime
from app import db

class Tenant(db.Model):
    __tablename__ = 'tenants'
    
    tenant_id = db.Column(db.Integer, primary_key=True)
    tenant_name = db.Column(db.String(255), nullable=False)
    schema_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, tenant_name, schema_name, created_at=None):
        self.tenant_name = tenant_name
        self.schema_name = schema_name
        self.created_at = created_at or datetime.utcnow()

    def as_dict(self):
        return {
            "tenant_id": self.tenant_id,
            "tenant_name": self.tenant_name,
            "schema_name": self.schema_name,
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"<Tenant {self.tenant_name}>"
