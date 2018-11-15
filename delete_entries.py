#!/usr/bin/env python

# This is a temporary file to practice deleting entries from the SQLite3 server
# with SQLAlchedy

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

### Setup done, now deleting an entry from database ###

# We know there's a spinach ice cream item on a menu, so find it, and confirm
# that it has been found by printing the restaurant name
spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
print(spinach.restaurant.name)

# Now delete the offending item
session.delete(spinach)
session.commit()

# Confirm by attempting to find the menu item again. This should give an error
more_spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
