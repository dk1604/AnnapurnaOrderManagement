import logging
import os
import secrets
import sys

from alembic import command
from alembic.config import Config
from flask import Flask

from Properties import db_type, host, port, user, password, database
from src.database import AdaptorFactory
from src.controller.routes import configure_routes
from src.database.PSQLAdapterImpl import PSQLAdapterImpl


def handle_exception(exc_type, exc_value, exc_tb):
    if exc_type == KeyboardInterrupt:
        sys.__excepthook__(exc_type, exc_value, exc_tb)
    else:
        # Custom behavior for uncaught exceptions (e.g., log it without printing the full stack trace)
        print(f"Handled exception: {exc_value}")

sys.excepthook = handle_exception

template_folder = os.path.join(os.getcwd(), 'src', 'templates')
static_folder = os.path.join(os.getcwd(), 'src', 'static')

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

app.secret_key = secrets.token_hex(16)
logging.basicConfig(level=logging.INFO)

configure_routes(app)

def run_db_migrations():
    logging.info("\n33.................")
    logging.info("Running Alembic migrations")
    try:
        alembic_cfg = Config("alembic.ini")  # Ensure the path is correct
        command.upgrade(alembic_cfg, "head")
        logging.info("Alembic migrations completed successfully")
    except Exception as e:
        logging.error(f"Error during migrations: {e}")


def initialize_engines():
    """Initialize the engines at service startup."""
    PSQLAdapterImpl.get_engine()


# Create a table for menu items (if it doesn't exist)
def create_table():
    logging.info("\n22.................")
    run_db_migrations()
    logging.info('\nsuccessfully menu table created')


if __name__ == '__main__':
    logging.info("\n11.................")
    create_table()  # Make sure the menu table is created
    initialize_engines()
    app.run(host='0.0.0.0', port=5000, debug=False)
