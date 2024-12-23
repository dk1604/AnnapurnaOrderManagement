import logging

from sqlalchemy.engine import row
from sqlalchemy.exc import SQLAlchemyError

from src.models.CanteenModels import menu_table_response


def fetch_all(session, model_class):
    if not session:
        logging.error("No active session. Please connect first.")
        return None

    try:
        results = session.query(model_class).all()
        logging.error("Fetched all records.")

        response_list = [
            menu_table_response(id=row[0].id, name=row[0].name, description=row[0].description, price=row[0].price)
        ]
        return response_list
    except SQLAlchemyError as e:
        logging.error(f"Error fetching all data: {e}")
        return None
