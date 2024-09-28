from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector
from injector import singleton
from app.extensions import db
from app.extensions import init_logging

# Import Controllers
from app.controllers.tenants_controller import tenant_bp
from app.controllers.customer_controller import customer_bp


# Import Services
from app.services.tenants_service import TenantService
from app.services.customer_service import CustomerService


def configure(binder):
    binder.bind(TenantService, to=TenantService, scope=singleton)



def create_app():
    app = Flask(__name__)

    @app.teardown_request
    def teardown_request(exception=None):
        db.session.remove()

    CORS(app)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    logger = init_logging()
    logger.info(f"API MOBILE INVOKE")

    # Register blueprints
    app.register_blueprint(tenant_bp, url_prefix='/api/v1')
    app.register_blueprint(customer_bp, url_prefix='/api/v1')

    FlaskInjector(app=app, modules=[configure])

    return app
