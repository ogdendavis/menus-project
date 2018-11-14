#!/usr/bin/env python

# This is a temporary file to practice manipulating the SQLite3 server with
# SQLAlchemy

# Import SQLAlchemy tools to connect to and communicate with database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import classes from database creation file
from database_setup import Base, Restaurant, MenuItem

# Connect to database
engine = create_engine('sqlite:///restaurantmenu.db')

# Connect class definitions from Base with corresponding tables in the database
Base.metadata.bind = engine

# Create a session (like a cursor in PostgreSQL) -- you'll stage and send
# commands and info to the database via the session
DBSession = sessionmaker(bind = engine)
session = DBSession()

# Create a new restaurant using the class from database_setup
myFirstRestaurant = Restaurant(name = "Pizza Palace")
# Add the new database to the session, and commit it to the database
session.add(myFirstRestaurant)
session.commit()

# Create a new menu item using the class from database_setup
# Note that we establish the relationship between this menu item and the
# restaurant we just created by using the Python variable that references the
# restaurant
myFirstMenuItem = MenuItem(name = "Cheese Pizza", description = "Made with all natural ingredients and fresh mozzarella", course = "Entree", price = "$8.99", restaurant = myFirstRestaurant)
# Add and commit the new menu item
session.add(myFirstMenuItem)
session.commit()
