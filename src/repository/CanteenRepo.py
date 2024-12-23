import logging

from src.dao.CanteenDao import fetch_all, fetch_one
from src.database.PSQLAdapterImpl import SessionFactory


def get_index_route_repo():
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

