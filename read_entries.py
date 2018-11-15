#!/usr/bin/env python

# This is a temporary file to practice reading from the SQLite3 server with
# SQLAlchedy

### Setup on lines 8 - 24 is identical to setup in add_entries.py ###

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

### Setup done, now reading entries from database ###

# Take first row from a table and put it in a variable!
firstResult = session.query(Restaurant).first()
print(firstResult)
print(firstResult.name)

# Take all the rows in the Restaurant table, and put them in a Python object.
# I'm doing this in two steps so I can access attributes of the query itself,
# as well as the result
restaurant_query = session.query(Restaurant)
restaurants = restaurant_query.all()

# Show description of columns in the query
print(restaurant_query.column_descriptions)

# Print the name for each restaurant in the result
for restaurant in restaurants:
    print restaurant.name

# Restaurants in alphabetical order by name
restaurants_in_alpha = restaurant_query.order_by('name').all()
for restaurant in restaurants_in_alpha:
    print(restaurant.name)
