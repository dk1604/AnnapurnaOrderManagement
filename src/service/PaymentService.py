import logging

import requests
import Properties

x_api_version = "2023-08-01"


def get_cashfree_payment_session(order_data):
    logging.error("customer data .............%s", order_data)
    url = 'https://sandbox.cashfree.com/pg/orders'
    headers = {
        'Content-Type': 'application/json',
        'x-client-id': Properties.client_id,
        'x-client-secret': Properties.client_secret,
        'x-api-version': x_api_version
    }
    response = requests.post(url, json=order_data, headers=headers)
    logging.error("**cashfree** response is:: %s", response.json())

    if response.status_code == 200:
        data = response.json()
        logging.error("payment session id data 1 %s", data)
        logging.error("payment session id data 2 %s", data.get('payment_session_id'))
        # Check if the payment URL was generated successfully
        if data.get('order_status') == 'ACTIVE':
            return data.get('payment_session_id')
        else:
            return None
