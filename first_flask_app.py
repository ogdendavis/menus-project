#!/usr/bin/env python

# Simple flask app to learn the framework
from flask import Flask

# Create an instance of Flask, using the application name assigned to this
# module by Python
app = Flask(__name__)

# Import SQLAlchemy tools to connect to and communicate with database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import classes from database creation file
from database_setup import Base, Restaurant, MenuItem

# Connect to database and connect tables to Base classes
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

# Create a sessionmaker -- each function will create its own session
DBSession = sessionmaker(bind = engine)

# @app.route tells Flask to execute the following function when it receives
# a GET request to the indicated path. You can chain them as shown
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def showMenu(restaurant_id = 1):
    # We've provided a default parameter of 1, like in JavaScripts
    # This will display all menu items for a restaurant
    session = DBSession()
    # Query for restaurant, by id. Returns object with restaurant name
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    # Query for menu items of restaurant. Returns object with all items.
    menu_items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    # Now that we have the menu items, print everything out!
    output = ''
    output += '<h1>{}</h1>'.format(restaurant.name)
    output += '<h2>Current Menu:</h2>'
    output += '<ul>'
    for item in menu_items:
        output += '<li>{}'.format(item.name)
        output += '<ul><li>{}</li>'.format(item.price)
        output += '<li>{}</li></ul>'.format(item.description)
    output += '</ul>'
    # Flask handles all the headers, wfile, etc. - so just return the content!
    return output

# If module is executed from the Python shell, do this stuff. If it's imported
# into some other code, don't do this stuff!
if __name__ == '__main__':
    # Debug mode makes server reload whenever code change is detected! No need
    # to stop and restart server whenever we want to see a change.
    app.debug = True
    # Serve on all public IP addresses, on port 5000
    app.run(host = '0.0.0.0', port = 5000)
