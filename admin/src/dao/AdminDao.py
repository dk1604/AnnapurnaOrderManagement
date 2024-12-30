import logging

from admin.src.models.AdminModel import CanteenMenu


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
