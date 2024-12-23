import logging
import os

from flask import request, redirect, url_for, render_template, Flask
from flask.sansio.blueprints import Blueprint

from src.service.Service import get_index_route_data, get_order_item_by_id

routes_blueprint = Blueprint("routes", __name__)
logging.basicConfig(level=logging.INFO)


template_folder = os.path.join(os.getcwd(), 'src', 'templates')
static_folder = os.path.join(os.getcwd(), 'src', 'static')
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)


def configure_routes(app):
    @app.route('/')
    def index():
        logging.error("inside default route")
        try:
            menu_items = get_index_route_data()

            # conn.disconnect()
            if not menu_items:  # If the list is empty
                logging.error("menu items are none")
                # return "hello 1"
                return render_template('index.html', menu_items=None)  # Pass `None` or empty list

            # If the menu is not empty, render the template with data
            logging.error("menu_items........", menu_items)
            return render_template('index.html', menu_items=menu_items)
            # return "hello 2"
        except Exception as e:
            logging.error("exception at getting index......%s", str(e))

    # Order route
    @app.route('/order/<int:item_id>', methods=['GET', 'POST'])
    def order(item_id):
        logging.error("100..........", item_id)
        item = get_order_item_by_id(item_id)
        logging.error("item............%s", item)

        if request.method == 'POST':
            logging.error("101................")
            # Here you can add order functionality (e.g., save the order)
            name = request.form['name']
            quantity = request.form['quantity']
            logging.error("name....", name)
            logging.error("quantity....", quantity)
            logging.error("item....", item['name'])
            # You can save this to an "orders" table or send a confirmation email
            return redirect(url_for('index'))

        return render_template('order.html', item=item)
