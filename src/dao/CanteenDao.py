import logging
import sys

from src.database.PSQLAdapterImpl import Menu
from src.models.CanteenModels import menu_table_response

def handle_exception(exc_type, exc_value, exc_tb):
    if exc_type == KeyboardInterrupt:
        sys.__excepthook__(exc_type, exc_value, exc_tb)
    else:
        # Custom behavior for uncaught exceptions (e.g., log it without printing the full stack trace)
        print(f"Handled exception: {exc_value}")

sys.excepthook = handle_exception


def fetch_all(session):
    try:
        records = session.query(Menu).all()
        logging.error("Fetched all records.")

        response_list = [
            #menu_table_response(id=row.id, name=row.name, description=row.description, price=row.price) for row in records
            menu_table_response(id=row.id, name=row.name, price=row.price) for row in records
        ]
        logging.error("Fetched response_list_db %s", response_list)
        return response_list
    except Exception as e:
        logging.error(f"Error fetching all data: {e}")
        return None


def fetch_all_by_food_category(session, food_category):
    try:
        records = session.query(Menu).filter(Menu.food_category == food_category).all()
        logging.error("Fetched all records for food category: ", food_category)

        response_list = [
            #menu_table_response(id=row.id, name=row.name, description=row.description, price=row.price) for row in records
            menu_table_response(id=row.id, name=row.name, price=row.price) for row in records
        ]
        logging.error("Fetched response_list_db %s", response_list)
        return response_list
    except Exception as e:
        logging.error(f"Error fetching all data: {e}")
        return None


def fetch_one(session, item_id):
    try:
        record = session.query(Menu).filter(Menu.id == item_id).first()
        if not record:
            logging.error('no record found for: ',item_id)
            raise ValueError("Error: no record found for")
        else:
            #response = menu_table_response(id=record.id, name=record.name, description=record.description, price=record.price)
            response = menu_table_response(id=record.id, name=record.name, price=record.price)
            return response
    except Exception as err:
        session.rollback()
        logging.error(f'error occurred during get by id dao: {str(err)}')
        raise ValueError(f"Error: {err}")

