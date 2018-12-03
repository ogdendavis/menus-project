#!/usr/bin/env python

# This module will create the database being used for the project.
# Dependencies: SQLAlchemy, SQLite3

### Configuration code: Setup and import of dependencies ###

import os

# Sys provides ability to manipulate runtime environment
import sys

# SQLAlchemy is an ORM that allows communication between Python code and SQL
# database using objects, instead of relying on strings
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Declarative base alerts SQLAlchemy that classes created in this module
# correspond to tables in the database
Base = declarative_base()


### Class code: Create classes to represent tables in SQL database ###

class Restaurant(Base):
    __tablename__ = 'restaurant'
    # Define columns within the table
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

    # Serializer to use in exporting JSON objects
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }


class MenuItem(Base):
    __tablename__ = 'menu_item'
    # Define columns within the table
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    # Note that price is a STRING, not a numeric value
    price = Column(String(8))
    # Create foreign key relationship between restaurant and menu_item
    # restaurant_id is populated from restaurant table
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    # This creates the relationship between the class attribute 'restaurant'
    # and the Restaurant class. When you create a new menu item, you'll pass
    # a reference to the restaurant to which the menu item belongs in this
    # 'restaurant' attribute.
    restaurant = relationship(Restaurant)

    ### Adding a serializer to make JSON objects from MenuItem database ###
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'course': self.course,
            'description': self.description,
            'price': self.price,
            'restaurant': self.restaurant_id
        }


### Final setup ###

# Create new SQLite3 database
engine = create_engine('sqlite:///restaurantmenu.db')

# Add classes above as tables in database
Base.metadata.create_all(engine)
