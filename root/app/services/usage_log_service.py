import logging
from flask_injector import inject
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db

logger = logging.getLogger(__name__)

class UsageLogService:

    @inject
    def __init__(self):
        pass  # Si necesitas inyectar otros servicios, hazlo aquí

    def create_usage_log(self, action, performed_by=None):
        """
        Logs an action to the usage log.

        Args:
            action (str): The action performed.
            performed_by (str): The user who performed the action (optional).
        """
        try:
            logger.info(f"Logging action: {action} performed by: {performed_by}")
            # Aquí podrías guardar el registro en la base de datos si fuera necesario
            # Por ejemplo:
            # new_log = UsageLog(action=action, performed_by=performed_by)
            # db.session.add(new_log)
            # db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error logging action: {e}")
            raise
