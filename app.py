import logging
import os
import secrets
import sys

from alembic import command
from alembic.config import Config
from flask import Flask

from src.admin.controller.admin_routes import configure_admin_routes
from src.controller.order_routes import order_routes
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
logging.basicConfig(level=logging.INFO)

app.secret_key = secrets.token_hex(16)

configure_routes(app)
configure_admin_routes(app)
order_routes(app)


def run_db_migrations():
    logging.info("Running Alembic migrations")
    try:
        alembic_cfg = Config("alembic.ini")  # Ensure the path is correct
        command.upgrade(alembic_cfg, "head")
        logging.error("Alembic migrations completed successfully")
    except Exception as e:
        logging.error(f"Error during migrations: {e}")


def initialize_engines():
    """Initialize the engines at service startup."""
    PSQLAdapterImpl.get_engine()


# Create a table for menu items (if it doesn't exist)
def create_table():
    run_db_migrations()
    logging.error('successfully menu table created')


if __name__ == '__main__':
    create_table()  # Make sure the menu table is created
    initialize_engines()
    app.run(host='0.0.0.0', port=5050, debug=False)
