import logging

from src.database.PSQLAdapterImpl import Menu
from src.models.CanteenModels import menu_table_response


def fetch_all(session):
    try:
        records = session.query(Menu).all()
        logging.error("Fetched all records.")

        response_list = [
            menu_table_response(id=row.id, name=row.name, description=row.description, price=row.price) for row in records
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
            response = menu_table_response(id=record.id, name=record.name, description=record.description, price=record.price)
            return response
    except Exception as err:
        session.rollback()
        logging.error(f'error occurred during get by id dao: {str(err)}')
        raise ValueError(f"Error: {err}")

