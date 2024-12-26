import logging
import os
import sys

import requests
from flask import request, redirect, url_for, render_template, Flask, session
from flask.sansio.blueprints import Blueprint

import Properties
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
            quantity = int(request.form['quantity'])
            logging.error("name, quantity, item, price....%s, %s, %s, %s", name, quantity, item.name, item.price)
            logging.error("name, quantity, item, price....%s, %s, %s, %s", type(name), type(quantity), type(item.name), type(item.price))

            # logic to add item and quantity in cart and maintain session
            if 'cart' not in session:
                session['cart'] = []  # Initialize the cart if it doesn't exist

            # Check if the item already exists in the cart
            item_exists = False
            for cart_item in session['cart']:
                logging.error("cart item exist............%s", cart_item)
                if cart_item['id'] == item.id:
                    logging.error("cart item qty............%s", cart_item['quantity'])
                    cart_item['quantity'] += quantity  # Update the quantity if item is already in the cart
                    # cart_item['price'] += item.price  # Update the quantity if item is already in the cart
                    item_exists = True
                    break

            if not item_exists:
                logging.error("cart item not exist............")
                # If the item doesn't exist in the cart, add it
                session['cart'].append({
                    'id': item.id,
                    'name': item.name,
                    'quantity': quantity,
                    'price': item.price
                })
            # Log the cart for debugging purposes
            logging.error("Updated cart: %s", session['cart'])

            # Save session data
            session.modified = True

            # You can save this to an "orders" table or send a confirmation email
            return redirect(url_for('food_preference'))

        return render_template('order.html', item=item)

    @app.route('/cart')
    def cart():
        cart_items = session.get('cart', [])
        return render_template('cart.html', cart_items=cart_items)

    @app.route('/checkout', methods=['GET', 'POST'])
    def checkout():
        cart_items = session.get('cart', [])

        # If the form is submitted, initiate payment
        if request.method == 'POST':
            total_amount = sum(item['quantity'] * item['price'] for item in cart_items)

            try:
                order_data = {
                    'order_amount': total_amount,
                    'order_currency': 'INR',
                    'order_id': 'unique_order_id',  # Unique Order ID
                    'order_note': 'Your order from Annapurna',
                    'customer_details': {
                        'customer_id': 'customer_123',
                        'customer_phone': '9999999999',
                        'customer_email': 'customer@example.com'
                    }
                }
                payment_url = create_payment_url(order_data)

                if payment_url:
                    return redirect(payment_url)
            except Exception as e:
                logging.error("error at CashfreeImpl %s", e)

        return render_template('checkout.html', cart_items=cart_items)

    def create_payment_url(order_data):
        url = 'https://api.cashfree.com/pg/orders'
        headers = {
            'Content-Type': 'application/json',
            'x-client-id': Properties.client_id,
            'x-client-secret': Properties.client_secret
        }
        response = requests.post(url, json=order_data, headers=headers)
        logging.error("**cashfree** response is:: %s", response.json())

        if response.status_code == 200:
            data = response.json()
            # Check if the payment URL was generated successfully
            if data.get('status') == 'OK':
                return data.get('payment_link')  # Cashfree payment URL
        return None
