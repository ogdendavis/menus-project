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
@app.route('/hello')
def HelloWorld():
    # This will get the first restaurant, and display all its menu items
    session = DBSession()
    first_restaurant = session.query(Restaurant).order_by('name').first()
    menu_items = session.query(MenuItem).filter_by(restaurant_id = first_restaurant.id).all()
    # Now that we have the menu items, print everything out!
    output = ''
    output += '<h1>{}</h1>'.format(first_restaurant.name)
    output += '<ul>'
    for item in menu_items:
        output += '<li>{}</li>'.format(item.name)
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
