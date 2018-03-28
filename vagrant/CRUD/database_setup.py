# SQLAlchemy has: configuration, class, table, and mapper sections

### Configuration: import necessary modules, creates declarative base instance
# to access SQLAlchemy features

# sys interacts with the Python interpreter
import sys

# Import classes for mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

# SQLAlchemy's declarative allows a Table, a mapper and a class object to be
# defined at once in one class definition for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# Creates foreign key relationships for mapper code
from sqlalchemy.orm import relationship

# For configuration code
from sqlalchemy import create_engine

# Makes our classes SQLAlchemy classes that correspond with tables in the database
Base = declarative_base()


### Class: OOP representation of tables in database
### Table: names tables
### Mapper: creates variables that create columns in database

# our class inherits from declarative_base
class Restaurant(Base):
    # name of table
    __tablename__ = 'restaurant'
    # create columns in table
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

class MenuItem(Base):
    __tablename__ = 'menu_item'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)


### Configuration: connects to db

# Point engine to database
engine = create_engine('sqlite:///restaurantmenu.db')

# Adds classes as new tables in database
Base.metadata.create_all(engine)
