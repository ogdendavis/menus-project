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

# Create a session (like a cursor in PostgreSQL)
DBSession = sessionmaker(bind = engine)
session = DBSession()

def read_names():
    names_list = []
    # Pull all restaurant names, in alpha order, into list
    for name in session.query(Restaurant.name).order_by('name'):
        # Even though we're only getting the name, it still arrives as an
        # object, so we have to pull out the first entry to get the name string
        names_list.append(name[0])

    # Return Python list of restaurant names
    return names_list
