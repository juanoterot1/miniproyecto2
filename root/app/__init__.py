from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector
from injector import singleton
from app.extensions import db
from app.extensions import init_logging

# Import Controllers
from .controllers.tenants_controller import tenant_bp
from .controllers.customer_controller import customer_bp
from .controllers.order_controller import order_bp
from .controllers.order_item_controller import order_item_bp
from .controllers.product_controller import product_bp
from .controllers.sales_controller import sale_bp
from .controllers.credit_account_controller import credit_account_bp
from .controllers.inventory_controller import inventory_bp

# Import Services
from .services.tenants_service import TenantService
from .services.customer_service import CustomerService
from .services.order_service import OrderService
from .services.order_item_service import OrderItemService
from .services.product_service import ProductService
from .services.sale_service import SaleService
from .services.credit_account_service import CreditAccountService
from .services.inventory_service import InventoryService

def configure(binder):
    binder.bind(TenantService, to=TenantService, scope=singleton)
    binder.bind(CustomerService, to=CustomerService, scope=singleton)
    binder.bind(OrderService, to=OrderService, scope=singleton)
    binder.bind(OrderItemService, to=OrderItemService, scope=singleton)
    binder.bind(ProductService, to=ProductService, scope=singleton)
    binder.bind(SaleService, to=SaleService, scope=singleton)
    binder.bind(CreditAccountService, to=CreditAccountService, scope=singleton)
    binder.bind(InventoryService, to=InventoryService, scope=singleton)

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    logger = init_logging()
    logger.info(f"API INVOKE")

    # Register blueprints
    app.register_blueprint(tenant_bp, url_prefix='/api/v1')
    app.register_blueprint(credit_account_bp, url_prefix='/api/v1')
    app.register_blueprint(customer_bp, url_prefix='/api/v1')
    app.register_blueprint(order_bp, url_prefix='/api/v1')
    app.register_blueprint(order_item_bp, url_prefix='/api/v1')
    app.register_blueprint(product_bp, url_prefix='/api/v1')
    app.register_blueprint(sale_bp, url_prefix='/api/v1')
    app.register_blueprint(inventory_bp, url_prefix='/api/v1')

    FlaskInjector(app=app, modules=[configure])

    return app
