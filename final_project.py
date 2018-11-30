#!/usr/bin/env python

# Dependencies: Flask, SQLAlchemy, SQLite3
# Uses database created in database_setup.py, and expanded by lotsofmenus.py
from flask import Flask, render_template, request

# Set up Flask instance
app = Flask(__name__)

### Temporary dummy data to use in render_template so that I can set up the
### templates before setting up the database functionality:

#Fake Restaurants
f_restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
f_restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
f_item = {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree', 'id':'1'}
f_items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]


# Routes!
# Homepage - shows all restaurants
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    return render_template('restaurants.html', restaurants = f_restaurants)


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
    if request.method == 'POST':
        return 'Successful post to /restaurants/x/edit/'
    if request.method == 'GET':
        return render_template('editrestaurant.html', restaurant = f_restaurant)


# Delete a restaurant
@app.route('/restaurants/<int:restaurant_id>/delete/', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    if request.method == 'POST':
        return 'Successful post to /restaurants/x/delete/'
    if request.method == 'GET':
        return render_template('deleterestaurant.html', restaurant = f_restaurant)


# Show a restaurant's full menu
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    return render_template('menu.html', restaurant = f_restaurant, items = f_items)


# Add a menu item to a restaurant's menu
@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods = ['GET', 'POST'])
@app.route('/restaurants/<int:restaurant_id>/menu/add/', methods = ['GET', 'POST'])
def addItem(restaurant_id):
    if request.method == 'POST':
        return 'Successful POST to /restaurants/x/menu/add/'
    if request.method == 'GET':
        return render_template('additem.html', restaurant = f_restaurant)


# Edit a menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/edit/', methods = ['GET', 'POST'])
def editItem(restaurant_id, item_id):
    if request.method == 'POST':
        return 'Successful POST to /restaurants/x/menu/y/edit/'
    if request.method == 'GET':
        return render_template('edititem.html', restaurant = f_restaurant, item = f_item)


#Delete a menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/delete/', methods = ['GET', 'POST'])
def deleteItem(restaurant_id, item_id):
    if request.method == 'POST':
        return 'Successful POST to /restaurants/x/menu/y/delete'
    if request.method == 'GET':
        return render_template('deleteitem.html', restaurant = f_restaurant, item = f_item)


# When running as the web server, run in debug mode on localhost, port 5000
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
