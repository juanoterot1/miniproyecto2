from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.sales_reports import SalesReport

class SalesReportRepository:
    
    @staticmethod
    def create_sales_report(report_type, total_sales, id_customer, report_date=None, 
                            most_sold_product=None, least_sold_product=None, pending_collections=None):
        try:
            new_report = SalesReport(
                report_type=report_type,
                total_sales=total_sales,
                id_customer=id_customer,
                report_date=report_date,
                most_sold_product=most_sold_product,
                least_sold_product=least_sold_product,
                pending_collections=pending_collections
            )
            db.session.add(new_report)
            db.session.commit()
            return new_report
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_sales_report_by_id(report_id):
        try:
            return SalesReport.query.get(report_id)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def delete_sales_report(report_id):
        try:
            report = SalesReport.query.get(report_id)
            if report is None:
                return None

            db.session.delete(report)
            db.session.commit()
            return report
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
