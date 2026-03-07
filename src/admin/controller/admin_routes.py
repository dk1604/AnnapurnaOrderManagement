import json
import logging
import os
import sys
from http import HTTPStatus

from flask import Flask, request, Response
from flask.sansio.blueprints import Blueprint

from src.admin.models.AdminModel import CanteenMenu, VendorExpenseModel
from src.admin.service.AdminService import save_service, save_all_service, save_vendor_expense_service, \
    get_vendor_expense_service, get_all_menu_service
from src.service.Service import get_all_options_by_food_category

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

    @app.route('/save/all', methods=['POST'])
    def create_basic_food_menu():
        logging.error("inside create_basic_food_menu api")

        response = save_all_service()

        return response, HTTPStatus.OK

    @app.route('/order/vendor-expenses', methods=['POST'])
    def add_or_update_vendor_expense():
        try:
            print("inside add_or_update_vendor_expense api")
            logging.error("inside add_or_update_vendor_expense api")
            if request.data == b'':
                logging.error('Error occurred due to missing required request body')
                return Response(json.dumps({"reason": "Invalid request body"}), status=400, mimetype="application/json")
            else:
                logging.error("request response is not empty")
                input_json = request.get_json(force=True)
                logging.error("input............%s", input_json)
                data = VendorExpenseModel(**input_json)
                logging.error("request response is input_json %s", data)
                response = save_vendor_expense_service(data)

                return response.dict(), HTTPStatus.OK
        except Exception as e:
            logging.error("get_vendor_expense route failed............%s", str(e))

    @app.route('/order/vendor-expenses', methods=['GET'])
    def get_vendor_expense():
        try:
            logging.error('inside get_vendor_expense api')
            response = get_vendor_expense_service()
            response_dicts = [item.model_dump() for item in response]

            return response_dicts, HTTPStatus.OK
        except Exception as e:
            logging.error("get_vendor_expense route failed............%s", str(e))

    @app.route('/order/menu-items', methods=['GET'])
    def get_menu():
        try:
            logging.error('inside get_menu api')
            response = get_all_menu_service()
            response_dicts = [item.model_dump() for item in response]

            return response_dicts, HTTPStatus.OK
        except Exception as e:
            logging.error("get_menu route failed............%s", str(e))
