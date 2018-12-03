#!/usr/bin/env python

# Dependencies: Flask, SQLAlchemy, SQLite3
# Uses database created in database_setup.py, and expanded by lotsofmenus.py

# Set up Flask instance
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

# Import SQLAlchemy tools
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import classes from database creation file
from database_setup import Base, Restaurant, MenuItem

# Connect to database and connect tables to Base classes
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

# Create a database session to use in the app
DBSession = sessionmaker(bind = engine)
session = DBSession()


# Routes!
# Homepage - shows all restaurants
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)


# Add a new restaurant
@app.route('/restaurants/new/', methods = ['GET', 'POST'])
@app.route('/restaurants/add/', methods = ['GET', 'POST'])
def addRestaurant():
    # In Flask, can access data sent in HTTP request with request object. Useful
    # for screening by method (GET vs POST), and for teasing out info submitted
    # in a form via request.form -- both of which are done below
    if request.method == 'POST':
        new_restaurant = Restaurant(name = request.form['name'])
        session.add(new_restaurant)
        session.commit()
        # Flash a message confirming the change when user redirects to main page
        flash("{} created".format(new_restaurant.name))
        return redirect(url_for('showRestaurants'))
    if request.method == 'GET':
        return render_template('addrestaurant.html')


# Edit a restaurant
@app.route('/restaurants/<int:restaurant_id>/edit/', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
    # For GET or POST, we'll need the restaurant
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        flash("{} updated".format(restaurant.name))
        return redirect(url_for('showRestaurants'))
    if request.method == 'GET':
        return render_template('editrestaurant.html', restaurant = restaurant)


# Delete a restaurant
@app.route('/restaurants/<int:restaurant_id>/delete/', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash("{} deleted".format(restaurant.name))
        return redirect(url_for('showRestaurants'))
    if request.method == 'GET':
        return render_template('deleterestaurant.html', restaurant = restaurant)


# Show a restaurant's full menu
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return render_template('menu.html', restaurant = restaurant, items = items)


# Add a menu item to a restaurant's menu
@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods = ['GET', 'POST'])
@app.route('/restaurants/<int:restaurant_id>/menu/add/', methods = ['GET', 'POST'])
def addItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        # Note that here, as in addRestaurant, we don't need to provide a
        # unique ID for the new thing -- the database does that for us
        new_item = MenuItem(name = request.form['name'], course = request.form['course'], description = request.form['description'], price = request.form['price'], restaurant_id = restaurant_id)
        session.add(new_item)
        session.commit()
        flash("{} added".format(new_item.name))
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    if request.method == 'GET':
        return render_template('additem.html', restaurant = restaurant)


# Edit a menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/edit/', methods = ['GET', 'POST'])
def editItem(restaurant_id, item_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(id = item_id).one()
    if request.method == 'POST':
        # When I try to use a 'for name, value in item' loop, I get an error
        # that MenuItem objects aren't iterable. So I'm manually going over
        # each value in the object and setting it to the value that was given
        # in the form -- since I'm doing it manually, checking first and then
        # setting seems silly
        item.name = request.form['name']
        item.course = request.form['course']
        item.description = request.form['description']
        item.price = request.form['price']
        session.add(item)
        session.commit()
        flash("{} updated".format(item.name))
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    if request.method == 'GET':
        return render_template('edititem.html', restaurant = restaurant, item = item)


#Delete a menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/delete/', methods = ['GET', 'POST'])
def deleteItem(restaurant_id, item_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(id = item_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("{} deleted".format(item.name))
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    if request.method == 'GET':
        return render_template('deleteitem.html', restaurant = restaurant, item = item)


### Endpoints for JSON requests ###

# JSON object with one menu item:
@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/json/')
def exportItem(restaurant_id, item_id):
    # Get the item from the database
    item = session.query(MenuItem).filter_by(id = item_id).one()
    # Check that item exists at the restaurant indicated by the path
    if restaurant_id != item.restaurant_id:
        return 'No such item at this restaurant'
    # Return serialized JSON object containing this one menu item
    return jsonify(MenuItem = item.serialize)


# JSON object with a restaurant's entire menu
@app.route('/restaurants/<int:restaurant_id>/menu/json/')
def exportMenu(restaurant_id):
    # Get all items at the restaurant
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    # Loop through menu items and serialize them from within the jsonify caller
    return jsonify(MenuItem = [i.serialize for i in items])


# JSON object listing all restaurants with their ids
@app.route('/restaurants/json')
def exportRestaurants():
    # Get all restaurants from database
    restaurants = session.query(Restaurant).all()
    # Return all restaurants, using loop like in exportMenu
    return jsonify(Restaurant = [r.serialize for r in restaurants])


# When running as the web server, run in debug mode on localhost, port 5000
if __name__ == '__main__':
    # Secret key enables sessions, which lets message flashing work! In theory,
    # this should be a secure key -- but this one isn't
    app.secret_key = 'omg_so_secret'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
