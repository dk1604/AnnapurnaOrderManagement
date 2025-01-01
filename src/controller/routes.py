import logging
import os
import random
import sys
import time

from flask import request, redirect, url_for, render_template, Flask, session, jsonify
from flask.sansio.blueprints import Blueprint

import Properties
import Constants
from src.service.PaymentService import get_cashfree_payment_session
from src.service.Service import get_order_item_by_id, get_all_options_by_food_category

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

    @app.route('/food_type', methods=['POST'])
    def food_type():
        logging.error("inside desert menu")
        try:
            food_type = request.form.get('foodType')
            menu_items = get_all_options_by_food_category(food_type)

            if not menu_items:  # If the list is empty
                logging.error("menu items are none")
                return render_template('index.html', menu_items=None)  # Pass `None` or empty list

            # Retrieve cart quantities from the session
            cart = session.get('cart', [])
            cart_quantities = {item['id']: item['quantity'] for item in cart}
            # If the menu is not empty, render the template with data
            logging.error("menu_items........%s", menu_items)
            return render_template('index.html', menu_items=menu_items, cart_quantities=cart_quantities)
        except Exception as e:
            logging.error("exception at getting desert......%s", str(e))

    @app.route('/order', methods=['GET', 'POST'])
    def order():
        logging.error("inside order route....")
        if request.method == 'POST':
            logging.error("inside order route POST....%s", request.form)
            # Get all item_id and quantity query parameters
            item_ids = request.form.getlist('item_id')
            quantities = request.form.getlist('quantity')
            logging.error("item_ids............%s", item_ids)
            logging.error("quantities............%s", quantities)

            if len(item_ids) != len(quantities):
                return "Mismatch between item_ids and quantities", 400

            # Ensure item_ids and quantities are valid
            item_data = []
            for item_id, quantity in zip(item_ids, quantities):
                try:
                    item_id = int(item_id)
                    quantity = int(quantity)
                    item = get_order_item_by_id(item_id)
                    if item is None:
                        return f"Item with ID {item_id} not found", 404

                    logging.error("item_data..........%s", item_data)
                    item_data.append({'id': item.id, 'name': item.name, 'quantity': quantity, 'price': item.price})
                except ValueError as e:
                    return f"Invalid input: {e}", 400

            # Add items to the cart
            if 'cart' not in session:
                session['cart'] = []

            for item in item_data:
                item_exists = False
                for cart_item in session['cart']:
                    logging.error("item exist %s", item)
                    if cart_item['id'] == item['id']:
                        cart_item['quantity'] = 0
                        cart_item['quantity'] += item['quantity']
                        logging.error("final cart_item['quantity'].............%s", cart_item['quantity'])
                        if cart_item['quantity'] == 0:
                            session['cart'].remove(item)
                        item_exists = True
                        break

                if not item_exists:
                    logging.error("item not exist %s", item)
                    session['cart'].append(item)

            # Log the updated cart
            logging.error("Updated cart: %s", session['cart'])

            # Save session data
            session.modified = True

            # Redirect to the next page (e.g., food preference or cart summary)
            return redirect(url_for('food_preference'))

        # Handle GET request to display the menu
        # Retrieve cart quantities from session
        cart = session.get('cart', [])
        cart_quantities = {item['item_id']: item['quantity'] for item in cart}
        return redirect(url_for('food_preference'))

    @app.route('/checkout', methods=['GET', 'POST'])
    def checkout():
        # Initialize the cart if it's not already in the session
        if 'cart' not in session:
            session['cart'] = []
            session['cart_timestamp'] = time.time()  # Store the timestamp of cart creation

        # Check if the cart is older than 5 minutes (300 seconds)
        current_time = time.time()
        cart_timestamp = session.get('cart_timestamp')

        if cart_timestamp and current_time - cart_timestamp > int(Properties.time_to_nullify_session):  # 300 seconds = 5 minutes
            logging.error("Cart session expired.")
            session.pop('cart', None)  # Clear the cart
            session.pop('cart_timestamp', None)  # Clear the timestamp
            return redirect(url_for('food_preference'))  # Redirect to the home page or a different route

        cart_items = session.get('cart', [])
        cart_total = sum(item['quantity'] * item['price'] for item in cart_items)

        timestamp = int(time.time())
        random_number = random.randint(1000, 9999)

        # If the form is submitted, initiate payment
        if request.method == 'POST':
            logging.error("inside checkout route of POST....")

            unique_order_id = f"ORD{timestamp}{random_number}"
            data = request.get_json()
            user_name = data.get('user_name')
            user_phone = data.get('user_phone')
            if user_name and user_phone:
                session['user_name'] = user_name
                session['user_phone'] = user_phone
                session['order_token'] = unique_order_id

            try:
                order_data = {
                    'order_amount': cart_total,
                    'order_currency': Constants.CURRENCY,
                    'order_id': unique_order_id,  # Unique Order ID
                    'order_note': 'Your order from Annapurna',
                    'customer_details': {
                        'customer_id': user_name,
                        'customer_phone': user_phone,
                        'customer_email': 'customer@example.com'
                    },
                    "order_meta": {
                        "return_url": f"{Properties.base_url}/payment/success?order_id={unique_order_id}"
                    }
                }
                payment_session_id = get_cashfree_payment_session(order_data)

                if payment_session_id:
                    return jsonify({'payment_session_id': payment_session_id})
                else:
                    return jsonify({'error': 'Error creating payment session'})
            except Exception as e:
                logging.error("error at CashfreeImpl %s", e)

        return render_template('checkout.html', cart_items=cart_items, cart_total=cart_total)

    @app.route('/payment/success', methods=['GET'])
    def payment_success():
        logging.error("==============Inside payment success====================")
        order_id = request.args.get('order_id')

        if order_id:
            order_token = session.get('order_token')  # Example of another parameter from Cashfree
            logging.error("session order token post payment success %s", order_token)
            user_name = session.get('user_name')
            user_phone = session.get('user_phone')
            logging.error("session user_name post payment success %s", user_name)
            logging.error("session user_phone post payment success %s", user_phone)
            logging.error("order successfully processed and order token generated %s", order_token)

            cart_items = session.get('cart', [])
            cart_total = sum(item['quantity'] * item['price'] for item in cart_items)

            logging.error("ORDER SUCCESS ***** cart_items %s", cart_items)
            logging.error("ORDER SUCCESS ***** cart_total %s", cart_total)
            logging.error("ORDER SUCCESS ***** order_token %s", order_token)

            # Clear cart session after successful payment
            session.pop('cart', None)
            session.pop('cart_timestamp', None)
            # session.pop('user_name', None)
            # session.pop('user_phone', None)

            return render_template('success.html', order_id=order_id, order_token=order_token)
        else:
            logging.error("no order_id found. Please place your order again. "
                          "Routing to main menu again. sorry for the inconvenience")
            return redirect(url_for('food_preference'))

    @app.route('/payment/failure', methods=['GET'])
    def payment_failure():
        # This could be the page to handle any failed payment cases.
        return render_template('failure.html', message="Payment failed. Please try again.")
