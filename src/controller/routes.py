import logging
import os
import sys

from flask import request, redirect, url_for, render_template, Flask
from flask.sansio.blueprints import Blueprint

from src.service.Service import get_all_options, get_order_item_by_id, get_all_options_by_food_category

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


def configure_routes(app):
    @app.route('/')
    def food_preference():
        logging.error("inside food preference route")
        return render_template('food_preference.html')

    # def index():
    #     logging.error("inside default route")
    #     try:
    #         menu_items = get_index_route_data()
    #
    #         if not menu_items:  # If the list is empty
    #             logging.error("menu items are none")
    #             return render_template('index.html', menu_items=None)  # Pass `None` or empty list
    #
    #         # If the menu is not empty, render the template with data
    #         logging.error("menu_items........", menu_items)
    #         return render_template('index.html', menu_items=menu_items)
    #     except Exception as e:
    #         logging.error("exception at getting index......%s", str(e))

    # Route for Veg
    @app.route('/veg')
    def veg():
        logging.error("inside veg menu")
        try:
            menu_items = get_all_options_by_food_category("veg")

            if not menu_items:  # If the list is empty
                logging.error("menu items are none")
                return render_template('index.html', menu_items=None)  # Pass `None` or empty list

            # If the menu is not empty, render the template with data
            logging.error("menu_items........", menu_items)
            return render_template('index.html', menu_items=menu_items)
        except Exception as e:
            logging.error("exception at getting index......%s", str(e))

    # Route for Non-Veg
    @app.route('/non_veg')
    def non_veg():
        logging.error("inside non_veg menu")
        try:
            menu_items = get_all_options_by_food_category("non_veg")

            if not menu_items:  # If the list is empty
                logging.error("menu items are none")
                return render_template('index.html', menu_items=None)  # Pass `None` or empty list

            # If the menu is not empty, render the template with data
            logging.error("menu_items........", menu_items)
            return render_template('index.html', menu_items=menu_items)
        except Exception as e:
            logging.error("exception at getting index......%s", str(e))\


    @app.route('/desert')
    def desert():
        logging.error("inside desert menu")
        try:
            menu_items = get_all_options_by_food_category("desert")

            if not menu_items:  # If the list is empty
                logging.error("menu items are none")
                return render_template('index.html', menu_items=None)  # Pass `None` or empty list

            # If the menu is not empty, render the template with data
            logging.error("menu_items........", menu_items)
            return render_template('index.html', menu_items=menu_items)
        except Exception as e:
            logging.error("exception at getting index......%s", str(e))

    # Route for All options
    @app.route('/all')
    def all_options():
        logging.error("inside all menu")
        try:
            # menu_items = get_all_options()
            menu_items = get_all_options_by_food_category("all")

            if not menu_items:  # If the list is empty
                logging.error("menu items are none")
                return render_template('index.html', menu_items=None)  # Pass `None` or empty list

            # If the menu is not empty, render the template with data
            logging.error("menu_items........", menu_items)
            return render_template('index.html', menu_items=menu_items)
        except Exception as e:
            logging.error("exception at getting index......%s", str(e))

    # Order route
    @app.route('/order/<int:item_id>', methods=['GET', 'POST'])
    def order(item_id):
        item = get_order_item_by_id(item_id)
        logging.error("item............%s", item)

        if request.method == 'POST':
            # Here you can add order functionality (e.g., save the order)
            name = request.form['name']
            quantity = request.form['quantity']
            logging.error("name, quantity, item....%s, %s, %s", name, quantity, item.name)

            # You can save this to an "orders" table or send a confirmation email
            return redirect(url_for('food_preference'))

        return render_template('order.html', item=item)
