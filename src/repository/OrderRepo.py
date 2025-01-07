import logging

from src.dao.CanteenDao import save_order_details, get_order_details_dao_by_time
from src.database.DbModels import CustomerOrder
from src.database.PSQLAdapterImpl import SessionFactory


def save_order_details_repo(customer_order_detail):
    try:
        get_session = SessionFactory.get_session()
        with get_session as session:
            with session.begin():
                menu_items = save_order_details(session, CustomerOrder(order_id=customer_order_detail.order_id,
                                                                       order_details=customer_order_detail.order_details,
                                                                       cart_price=customer_order_detail.cart_price,
                                                                       payment_mode=customer_order_detail.payment_mode,
                                                                       user_name=customer_order_detail.user_name,
                                                                       user_phone=customer_order_detail.user_phone,
                                                                       order_date=customer_order_detail.order_date))
                logging.error("44...........menu_items: %s", menu_items)
                return menu_items
    except Exception as ex:
        session.rollback()
        logging.error("45..exception occured in get all %s", str(ex))
        raise Exception(ex)
    finally:
        session.close()


def get_order_details_repo(start_time, end_time):
    try:
        get_session = SessionFactory.get_session()
        with get_session as session:
            with session.begin():
                return get_order_details_dao_by_time(session, start_time, end_time)
    except Exception as ex:
        session.rollback()
        logging.error("46..exception occured in get all %s", str(ex))
        raise Exception(ex)
    finally:
        session.close()
