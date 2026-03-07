import logging
import sys

from sqlalchemy import text

from src.admin.dao.AdminDao import save_dao, save_all_dao, save_vendor_expense_dao, get_vendor_expense_dao
from src.database.DbModels import menu, VendorExpense
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

def save_all_repo():
    try:
        sql_file_path = "db/db_script.sql"
        get_session = SessionFactory.get_session()
        logging.error("get_session successful")
        with get_session as session:
            with session.begin():
                with open(sql_file_path, "r") as f:
                    sql_content = f.read()

                # Split statements by semicolon
                statements = [stmt.strip() for stmt in sql_content.split(";") if stmt.strip()]
                for stmt in statements:
                    session.execute(text(stmt))

                logging.info(f"SQL file {sql_file_path} executed successfully.")
                return "successful"
    except Exception as ex:
        session.rollback()
        logging.error("exception occurred in save %s", str(ex))
        None
    finally:
        session.close()

def save_vendor_expense_repo(data):
    try:
        get_session = SessionFactory.get_session()
        logging.error("get_session successful")
        with get_session as session:
            with session.begin():
                vendor_expense = save_vendor_expense_dao(session, VendorExpense(vendor=data.vendor,
                                                             material=data.material,
                                                             amount=data.amount,
                                                             payment_mode=data.payment_mode,
                                                             date=data.date,
                                                             id=data.id))
                logging.error("vendor_expense...........vendor_expense: %s", vendor_expense)
                return vendor_expense
    except Exception as ex:
        session.rollback()
        logging.error("exception occurred in save_vendor_expense_repo %s", str(ex))
        None
    finally:
        session.close()

def get_vendor_expense_repo():
    try:
        get_session = SessionFactory.get_session()
        logging.error("get_session successful")
        with get_session as session:
            with session.begin():
                vendor_expense = get_vendor_expense_dao(session)
                logging.error("vendor_expense...........vendor_expense: %s", vendor_expense)
                return vendor_expense
    except Exception as ex:
        session.rollback()
        logging.error("exception occurred in get_vendor_expense_repo %s", str(ex))
        None
    finally:
        session.close()
