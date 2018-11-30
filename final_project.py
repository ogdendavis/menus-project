#!/usr/bin/env python

# Dependencies: Flask, SQLAlchemy, SQLite3
# Uses database created in database_setup.py, and expanded by lotsofmenus.py
from flask import Flask

# Set up Flask instance
app = Flask(__name__)


# Routes!
# Homepage - shows all restaurants
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    return 'This page will show all restaurants'


# Add a new restaurant
@app.route('/restaurants/new/')
def addRestaurant():
    return 'This is the page to add a new restaurant'


# Edit a restaurant
@app.route('/restaurants/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
    return 'This is the page to edit the restaurant with id number {}'.format(restaurant_id)


# Delete a restaurant
@app.route('/restaurants/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
    return 'This is the page to delete the restaurant with id number {}'.format(restaurant_id)


# Show a restaurant's full menu
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    return 'This is the page to show the menu for the restaurant with id number {}'.format(restaurant_id)


# Add a menu item to a restaurant's menu
@app.route('/restaurants/<int:restaurant_id>/menu/add/')
def addItem(restaurant_id):
    return 'This is the page to add a menu item for the restaurant with id number {}'.format(restaurant_id)


# Edit a menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/edit/')
def editItem(restaurant_id, item_id):
    return 'This is the page to edit menu item {} for restaurant {}'.format(item_id, restaurant_id)


#Delete a menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/delete/')
def deleteItem(restaurant_id, item_id):
    return 'This is the page to delete menu item {} from restaurant {}'.format(item_id, restaurant_id)


# When running as the web server, run in debug mode on localhost, port 5000
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
