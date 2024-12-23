import logging
import sys

from src.dao.CanteenDao import fetch_all, fetch_one, fetch_all_by_food_category
from src.database.PSQLAdapterImpl import SessionFactory


def handle_exception(exc_type, exc_value, exc_tb):
    if exc_type == KeyboardInterrupt:
        sys.__excepthook__(exc_type, exc_value, exc_tb)
    else:
        # Custom behavior for uncaught exceptions (e.g., log it without printing the full stack trace)
        print(f"Handled exception: {exc_value}")

sys.excepthook = handle_exception


def get_all_options_repo():
    try:
        get_session = SessionFactory.get_session()
        with get_session as session:
            with session.begin():
                menu_items = fetch_all(session)
                logging.error("menu_items...........menu_items: %s", menu_items)
                return menu_items
    except Exception as ex:
        session.rollback()
        logging.error("exception occured in get all %s", str(ex))
        raise Exception(ex)
    finally:
        session.close()


def get_all_options_by_food_category_repo(food_category):
    try:
        get_session = SessionFactory.get_session()
        with get_session as session:
            with session.begin():
                menu_items = fetch_all_by_food_category(session, food_category)
                logging.error("food_category menu_items...........menu_items: %s", menu_items)
                return menu_items
    except Exception as ex:
        session.rollback()
        logging.error("exception occured in get all %s", str(ex))
        raise Exception(ex)
    finally:
        session.close()


def get_order_item_by_id_repo(item_id):
    try:
        get_session = SessionFactory.get_session()
        with get_session as session:
            with session.begin():
                menu_items = fetch_one(session, item_id)
                logging.error("44...........menu_items: %s", menu_items)
                return menu_items
    except Exception as ex:
        session.rollback()
        logging.error("45..exception occured in get all %s", str(ex))
        raise Exception(ex)
    finally:
        session.close()

