import logging
import os

from flask import request, redirect, url_for, render_template, Flask
from flask.sansio.blueprints import Blueprint

from src.service.Service import get_index_route_data

routes_blueprint = Blueprint("routes", __name__)
logging.basicConfig(level=logging.INFO)


template_folder = os.path.join(os.getcwd(), 'src', 'templates')
static_folder = os.path.join(os.getcwd(), 'src', 'static')
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.logger.setLevel(logging.INFO)

def configure_routes(app):
    @app.route('/')
    def index():
        app.logger.info("inside default route")
        try:
            menu_items = get_index_route_data()

            # conn.disconnect()
            if not menu_items:  # If the list is empty
                app.logger.info("menu items are none")
                return "hello 1"
                # return render_template('index.html', menu_items=None)  # Pass `None` or empty list

            # If the menu is not empty, render the template with data
            # return render_template('index.html', menu_items=menu_items)
            return "hello 2"
        except Exception as e:
            app.logger.info("exception at getting index......%s", str(e))
            app.logger.error("exception at getting index......%s", str(e))

    # Order route
    # @app.route('/order/<int:item_id>', methods=['GET', 'POST'])
    # def order(item_id):
    #     logging.info("\n100..........", item_id)
    #     conn = get_db_connection()
    #     item = conn.fetch_one('SELECT * FROM menu WHERE id = %s', (item_id,))
    #     logging.info("item............%s", item)
    #
    #     if request.method == 'POST':
    #         logging.info("\n101................")
    #         # Here you can add order functionality (e.g., save the order)
    #         name = request.form['name']
    #         quantity = request.form['quantity']
    #         print("\nname....", name)
    #         print("\nquantity....", quantity)
    #         print("\nitem....", item['name'])
    #         # You can save this to an "orders" table or send a confirmation email
    #         return redirect(url_for('index'))
    #
    #     return render_template('order.html', item=item)
