import logging

from sqlalchemy.exc import SQLAlchemyError


def fetch_all(session, model_class):
    if not session:
        print("No active session. Please connect first.")
        return None

    try:
        results = session.query(model_class).all()
        print("Fetched all records.")
        return results
    except SQLAlchemyError as e:
        print(f"Error fetching all data: {e}")
        return None
