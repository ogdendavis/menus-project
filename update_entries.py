#!/usr/bin/env python

# This is a temporary file to practice updating entries in  the SQLite3 server
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

### Setup done, now updating entries in database ###

# Find all the veggie burgers!
all_veggie_burgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for burger in all_veggie_burgers:
    print(burger.id)
    print(burger.price)
    print(burger.restaurant.name)
    print('')

# Found that the most expensive burgers are at Panda Garden and Auntie Ann's.
# Let's say that Auntie Ann's wants to compete on price. The ID of their burger
# in the MenuItem database is 43
# .one() tells SQLALchemy that the query should only return one item
auntie_burger = session.query(MenuItem).filter_by(id = 43).one()
print('Selected burger:')
print(auntie_burger.id)
print(auntie_burger.price)
print(auntie_burger.restaurant.name)
print('')

# Now update the selected burger's price, add the cahnge to the session, and
# commit to the database
auntie_burger.price = '$6.75'
session.add(auntie_burger)
session.commit()

# Did the price change?
print('New Veggie Burger price at Auntie Ann\'s Diner:')
print(auntie_burger.price)

# It changed! Now everybody is pissed, and wants to make sure they undercut
# Auntie's price to stay competitive.
# I tried to filter out Auntie Ann's Diner by name, but that didn't work for
# some reason. So I queried to find out that Auntie Ann's id is 8, and am
# filtering by that!
for burger in all_veggie_burgers:
    price = float(burger.price[1:])
    if price >= 6.75 and burger.restaurant.id != 8:
        print(burger.restaurant.name)
        print('Old price: {}'.format(burger.price))
        burger.price = '$4.99'
        session.add(burger)
        session.commit()
        print('New price: {}'.format(burger.price))
        print('')
