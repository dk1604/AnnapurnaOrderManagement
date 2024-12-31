import json
import logging
import os
import sys
from http import HTTPStatus

from flask import Flask, request, Response
from flask.sansio.blueprints import Blueprint

from src.admin.src.models.AdminModel import CanteenMenu
from src.admin.src.service.AdminService import save_service

admin_routes_blueprint = Blueprint("admin_routes", __name__)
logging.basicConfig(level=logging.INFO)


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


def configure_admin_routes(app):
    @app.route('/save', methods=['POST'])
    def add_or_update_food_menu():
        logging.error("inside add_or_update_food_menu api")
        if request.data == b'':
            logging.error('Error occurred due to missing required request body')
            return Response(json.dumps({"reason": "Invalid request body"}), status=400, mimetype="application/json")
        else:
            logging.error("request response is not empty")
            input_json = request.get_json(force=True)
            logging.error("input............%s", input_json)
            data = CanteenMenu(**input_json)
            logging.error("request response is input_json %s", data)
            response = save_service(data)
            logging.error("response came............%s", type(response))

            return response.dict(), HTTPStatus.OK
