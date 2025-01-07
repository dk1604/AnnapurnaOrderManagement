import logging
import os
import sys
from datetime import datetime

from flask import Blueprint, Flask, request, jsonify, Response, render_template

from src.service.OrderService import get_order_details_service

routes_blueprint = Blueprint("routes", __name__)
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


def order_routes(app):
    @app.route('/order/summary', methods=['GET'])
    def order_summary():
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        try:
            if start_date:
                start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                print("start_date..........", start_date)
            if end_date:
                end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
                print("end_date............", end_date)
        except ValueError as e:
            return jsonify({"error": "Invalid datetime format. Use YYYY-MM-DD HH:MM:SS."}), 400

        if start_date and end_date and start_date >= end_date:
            return jsonify({"error": "start_date must be older than end_date."}), 400

        start_epoch = int(start_date.timestamp()) if start_date else "Not specified"
        end_epoch = int(end_date.timestamp()) if end_date else "Not specified"

        response_list = get_order_details_service(start_epoch, end_epoch)

        response_dict = [response.dict() for response in response_list]
        print('\nresponse_dict..................', response_dict)

        return jsonify(response_dict)

    @app.route('/order/dashboard')
    def index():
        return render_template('order_details.html')
