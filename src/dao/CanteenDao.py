import logging

from src.models.CanteenModels import menu_table_response


def fetch_all(session, model_class):
    try:
        logging.error("model_class is: ", model_class)
        records = session.query(model_class).all()
        logging.error("Fetched all records.")

        response_list = [
            menu_table_response(id=row[0].id, name=row[0].name, description=row[0].description, price=row[0].price
                                ).model_dump() for row in records
        ]
        logging.error("Fetched response_list %s", response_list)
        return response_list
    except Exception as e:
        logging.error(f"Error fetching all data: {e}")
        return None
