#!/usr/bin/env python

# This module returns restaurant names as a list
# Dependencies: SQLite3, SQLAlchemy 1.2

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

def get_restaurants():
    # Create a session for this database transaction
    session = DBSession()
    # Pull all restaurants into a Python object, in alpha order
    restaurants = session.query(Restaurant).order_by('name').all()
    # Close session
    session.close()
    # Return Python list of restaurant names
    return restaurants

def get_restaurant_by_id(id):
    # Create a session for this transaction
    session = DBSession()
    # Query for one restaurant result, by id
    target_restaurant = session.query(Restaurant).filter_by(id = id).one()
    # Close session
    session.close()
    # Return object for target restaurant
    return target_restaurant

def add_restaurant(new_name):
    # Create a session for this database transaction
    session = DBSession()
    # Use Restaurant class from database_setup to create new restaurant object
    new_restaurant = Restaurant(name = new_name)
    # Add new restaurant object to the DB session
    session.add(new_restaurant)
    # Commit makes the change in the session, close closes it
    session.commit()
    session.close()

def edit_restaurant(id, new_name):
    # Create a session for this database transaction
    session = DBSession()
    # Get the indicated restaurant by ID, and update the name
    target = session.query(Restaurant).filter_by(id = id).one()
    target.name = new_name
    # Commit and close session
    session.commit()
    session.close()
