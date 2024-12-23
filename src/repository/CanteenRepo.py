import logging

from src.dao.CanteenDao import fetch_all
from src.database.PSQLAdapterImpl import SessionFactory, Menu


# from src.database.PSQLAdapterImpl import SessionFactory, Menu, PSQLAdapterImpl


def get_index_route_repo():
    try:
        logging.error("11.............")
        get_session = SessionFactory.get_session()
        with get_session as session:
            with session.begin():
                logging.error("12.............")
                menu_items = fetch_all(session, Menu)
                logging.error("5.........")
                logging.error("menu_items...........menu_items: %s", menu_items)
                return menu_items
    except Exception as ex:
        session.rollback()
        logging.error("exception occured in get all %s", str(ex))
        raise Exception(ex)
    finally:
        session.close()

