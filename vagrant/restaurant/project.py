from flask import Flask

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>')
def restaurant_menu(restaurant_id = None):
    # Get restaurant object representing first restaurant
    restaurant = session.query(Restaurant).first()
    # Get list of first restaurant's items as objects
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    output = ""
    # List each item's name, price, and description
    for i in items:
        output += i.name
        output += "<br>"
        output += i.price
        output += "<br>"
        output += i.description
        output += "<br><br>"
    return output

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/new-item/<int:restaurant_id>')
def newMenuItem(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/edit-item/<int:restaurant_id>/<int:menu_id>')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/delete-item/<int:restaurant_id>/<int:menu_id>')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
