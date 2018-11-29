#!/usr/bin/env python

# Simple flask app to learn the framework
from flask import Flask, render_template, request, redirect, url_for

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
    # Query for restaurant, by id. Returns object with name & id
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    # Query for menu items of restaurant. Returns object with all items.
    menu_items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    # Close the database session
    session.close()
    # Now that we have the data, send it to our menu template
    # The first argument is template to use (in templates folder)
    # Additional arguments are values to pass to template
    return render_template('menu.html', restaurant = restaurant, menu_items = menu_items)


# Use methods in route to allow functions to respond to more than just GET
@app.route('/restaurants/<int:restaurant_id>/create/', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    # Get object with restaurant info (id & name)
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

    # For GET requests, just show the form
    if request.method == 'GET':
        # Close the session, since we have no more database functions to run
        session.close()
        return render_template('newmenuitem.html', restaurant = restaurant)

    #For POST requests, create the new item and show the updated menu
    if request.method == 'POST':
        # Use the class defined in database_setup to create a new menu item
        new_item = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        # Add the new item to the database session, commit, and close
        session.add(new_item)
        session.commit()
        session.close()
        # Redirect is a Flask function that does what it says!
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))


@app.route('/restaurants/<int:restaurant_id>/<int:item_id>/edit/', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, item_id):
    session = DBSession()
    # Get both restaurant and item
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(id = item_id).one()

    if request.method == 'GET':
        # GET request simply shows the form
        session.close()
        return render_template('editmenuitem.html', item = item, restaurant = restaurant)

    if request.method == 'POST':
        # Update the item, commit it, and redirect to the restaurant's menu
        item.name = request.form['new_name']
        session.add(item)
        session.commit()
        session.close()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))


@app.route('/restaurants/<int:restaurant_id>/<int:item_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, item_id):
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(id = item_id).one()

    if request.method == 'GET':
        session.close()
        return render_template('deletemenuitem.html', restaurant = restaurant, item = item)

    if request.method == 'POST':
        session.delete(item)
        session.commit()
        session.close()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))

    return "page to delete a menu item. Task 3 complete!"


# If module is executed from the Python shell, do this stuff. If it's imported
# into some other code, don't do this stuff!
if __name__ == '__main__':
    # Debug mode makes server reload whenever code change is detected! No need
    # to stop and restart server whenever we want to see a change.
    app.debug = True
    # Serve on all public IP addresses, on port 5000
    app.run(host = '0.0.0.0', port = 5000)
