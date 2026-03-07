import logging
from datetime import datetime, timezone

from src.admin.models.AdminModel import CanteenMenu, VendorExpenseModel
from src.admin.service.utility import parse_insert_statement
from src.database.DbModels import VendorExpense, menu
from src.models.CanteenModels import menu_table_response


def save_dao(session, event):
    logging.error("inside save_dao.............,%s", event)
    try:
        session.add(event)
        session.flush()
        response = CanteenMenu(id=event.id,
                               name=event.name,
                               description=event.description,
                               price=event.price,
                               food_category=event.food_category)
        logging.error(f'record saved successfully: {response}')
        return response

    except Exception as dbError:
        session.rollback()
        logging.error(f'Error during save: {str(dbError)}')
        raise None


def save_all_dao(session):
    logging.error("inside save_all_dao.............")
    try:
        with open("db/db_script.sql", "r") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if line.lower().startswith("insert into"):
                data = parse_insert_statement(line)
                if data:
                    menu_item = CanteenMenu(
                        name=data.get("name"),
                        description=data.get("description"),
                        price=data.get("price"),
                        food_category=data.get("food_category")
                    )
                    session.add(menu_item)
                    session.commit()

            logging.error(f'record saved_all successfully')
            return ""

    except Exception as dbError:
        session.rollback()
        logging.error(f'Error during save_all: {str(dbError)}')
        raise None


def save_vendor_expense_dao(session, event):
    logging.error("inside save_vendor_expense_dao:,%s", event)
    try:
        if event.id:
            existing = session.query(VendorExpense).filter(VendorExpense.id == event.id).first()
            if not existing:
                raise ValueError(f"VendorExpense with id {event.id} not found for update")


            # Auto-map other fields
            for key, value in vars(event).items():
                if key not in ("_sa_instance_state", "id", "date"):
                    setattr(existing, key, value)

            existing.date = event.date if event.date is not None else (existing.date or datetime.now(timezone.utc))

            session.flush()
            response = VendorExpenseModel(
                id=existing.id,
                vendor=existing.vendor,
                material=existing.material,
                amount=existing.amount,
                payment_mode=existing.payment_mode,
                date=existing.date
            )
            logging.info(f"Vendor expense updated successfully: {response}")
            return response
        else:
            if not event.date:
                event.date = datetime.now(timezone.utc)  # timezone-aware current datetime
            session.add(event)
            session.flush()
            response = VendorExpenseModel(id=event.id,
                                          vendor=event.vendor,
                                          material=event.material,
                                          amount=event.amount,
                                          payment_mode=event.payment_mode,
                                          date=event.date)
            logging.error(f'record vendor expense saved successfully: {response}')
            return response

    except Exception as dbError:
        session.rollback()
        logging.error(f'Error during save_vendor_expense_dao: {str(dbError)}')
        raise None


def get_vendor_expense_dao(session):
    try:
        logging.error("inside get_vendor_expense_dao")
        expenses = session.query(VendorExpense).order_by(VendorExpense.date.desc()).order_by(VendorExpense.date.desc()).all()
        print(f"expenses  {expenses}")
        return map_to_pydantic_manual(expenses)

    except Exception as dbError:
        session.rollback()
        logging.error(f'Error during get_vendor_expense_dao: {str(dbError)}')
        raise None


def get_all_menu_dao(session):
    try:
        logging.error("inside get_vendor_expense_dao")
        records = session.query(menu).all()
        logging.error("Fetched all menu items")

        response_list = [
            #menu_table_response(id=row.id, name=row.name, description=row.description, price=row.price) for row in records
            menu_table_response(id=row.id, name=row.name, price=row.price) for row in records
        ]
        logging.error("Fetched response_list_db %s", response_list)
        return response_list
    except Exception as e:
        logging.error(f"Error fetching all data: {e}")
        return None
        expenses = session.query(VendorExpense).order_by(VendorExpense.date.desc()).order_by(VendorExpense.date.desc()).all()
        print(f"expenses  {expenses}")
        return map_to_pydantic_manual(expenses)

    except Exception as dbError:
        session.rollback()
        logging.error(f'Error during get_vendor_expense_dao: {str(dbError)}')
        raise None

def map_to_pydantic_manual(expenses):
    result = []
    for e in expenses:
        result.append(
            VendorExpenseModel(
                id=e.id,
                vendor=e.vendor,
                material=e.material,
                amount=e.amount,
                payment_mode=e.payment_mode,
                date=e.date
            )
        )
    return result
