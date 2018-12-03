#!/usr/bin/env python

# Dependencies: Flask, SQLAlchemy, SQLite3
# Uses database created in database_setup.py, and expanded by lotsofmenus.py

# Set up Flask instance
from flask import Flask, render_template, request, redirect, url_for
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
    if request.method == 'POST':
        return 'successful post to /restaurants/add/'
    if request.method == 'GET':
        return render_template('addrestaurant.html')


# Edit a restaurant
@app.route('/restaurants/<int:restaurant_id>/edit/', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
    # For GET or POST, we'll need the restaurant
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        return 'Successful post to /restaurants/x/edit/'
    if request.method == 'GET':
        return render_template('editrestaurant.html', restaurant = restaurant)


# Delete a restaurant
@app.route('/restaurants/<int:restaurant_id>/delete/', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        return 'Successful post to /restaurants/x/delete/'
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
        return 'Successful POST to /restaurants/x/menu/add/'
    if request.method == 'GET':
        return render_template('additem.html', restaurant = restaurant)


# Edit a menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/edit/', methods = ['GET', 'POST'])
def editItem(restaurant_id, item_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(id = item_id).one()
    if request.method == 'POST':
        return 'Successful POST to /restaurants/x/menu/y/edit/'
    if request.method == 'GET':
        return render_template('edititem.html', restaurant = restaurant, item = item)


#Delete a menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/delete/', methods = ['GET', 'POST'])
def deleteItem(restaurant_id, item_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(id = item_id).one()
    if request.method == 'POST':
        return 'Successful POST to /restaurants/x/menu/y/delete'
    if request.method == 'GET':
        return render_template('deleteitem.html', restaurant = restaurant, item = item)


# When running as the web server, run in debug mode on localhost, port 5000
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
