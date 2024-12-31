import logging
import sys

from admin.src.dao.AdminDao import save_dao
from src.database.DbModels import menu
from src.database.PSQLAdapterImpl import SessionFactory


def handle_exception(exc_type, exc_value, exc_tb):
    if exc_type == KeyboardInterrupt:
        sys.__excepthook__(exc_type, exc_value, exc_tb)
    else:
        # Custom behavior for uncaught exceptions (e.g., log it without printing the full stack trace)
        print(f"Handled exception: {exc_value}")


sys.excepthook = handle_exception


def save_repo(data):
    try:
        get_session = SessionFactory.get_session()
        logging.error("get_session successful")
        with get_session as session:
            with session.begin():
                menu_items = save_dao(session, menu(name=data.name,
                                                    description=data.description,
                                                    price=data.price,
                                                    food_category=data.food_category))
                logging.error("menu_items...........menu_items: %s", menu_items)
                return menu_items
    except Exception as ex:
        session.rollback()
        logging.error("exception occurred in save %s", str(ex))
        None
    finally:
        session.close()
