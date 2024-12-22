import os

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

from Properties import db_type, host, port, user, password, database
from src.database import AdaptorFactory

app = Flask(__name__)


# Create a database connection
def get_db_connection():
    print("*** inside get_db_connection ***")
    db_adapter = AdaptorFactory.AdapterFactory.create_adapter(db_type, host, port, user, password, database)
    # Connect to the database
    db_adapter.connect()
    return db_adapter


# Create a table for menu items (if it doesn't exist)
def create_table():
    conn = get_db_connection()
    conn.execute_query('''
        CREATE TABLE IF NOT EXISTS menu_sjop (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            price DECIMAL(10, 2) NOT NULL
        )
    ''')

# Home route to display the menu
@app.route('/')
def index():
    try:
        print("\ninside default route")
        conn = get_db_connection()
        print("\n4.................", conn)
        menu_items = conn.fetch_all('SELECT * FROM menu')
        print("\n5.........")
        print("menu_items...........", menu_items)
        conn.disconnect()
        return render_template('index.html', menu_items=menu_items)
    except Exception as e:
        print("exception at getting index......", str(e))

# Order route
@app.route('/order/<int:item_id>', methods=['GET', 'POST'])
def order(item_id):
    print("\n100..........", item_id)
    conn = get_db_connection()
    item = conn.fetch_one('SELECT * FROM menu WHERE id = %s', (item_id,))
    print("item............", item)

    if request.method == 'POST':
        print("\n101................")
        # Here you can add order functionality (e.g., save the order)
        name = request.form['name']
        quantity = request.form['quantity']
        # You can save this to an "orders" table or send a confirmation email
        return redirect(url_for('index'))

    return render_template('order.html', item=item)


if __name__ == '__main__':
    create_table()  # Make sure the menu table is created
    app.run(host='0.0.0.0', port=port, debug=True)
    
