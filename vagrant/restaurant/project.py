from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/restaurants/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    # Get restaurant object
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    # Get list of first restaurant's items as objects
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)


@app.route('/restaurants/new-item/<int:restaurant_id>', methods = ['GET', 'POST'])
def new_item(restaurant_id):
    # Handle POST request
    if request.method == 'POST':
        # create a new MenuItem object with name from form and id from URL path
        new_menu_item = MenuItem(name=request.form['name'],
                            restaurant_id = restaurant_id)
        session.add(new_menu_item)
        session.commit()
        flash("The menu item '%s' was created!" % new_menu_item.name)
        return redirect(url_for('restaurant_menu', restaurant_id = restaurant_id))
    # Handle GET request
    return render_template('new_menu_item.html', restaurant_id = restaurant_id)


@app.route('/restaurants/edit-item/<int:restaurant_id>/<int:item_id>', methods = ['GET', 'POST'])
def edit_item(restaurant_id, item_id):
    item_to_edit = session.query(MenuItem).filter_by(id = item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            item_to_edit.name = request.form['name']
        session.add(item_to_edit)
        session.commit()
        flash("The menu item was renamed to '%s'!" % item_to_edit.name)
        return redirect(url_for('restaurant_menu', restaurant_id = restaurant_id))
    return render_template('edit_menu_item.html', restaurant_id = restaurant_id,
                            item_id = item_id, item_to_edit = item_to_edit)


@app.route('/restaurants/delete-item/<int:restaurant_id>/<int:item_id>', methods = ['GET', 'POST'])
def delete_item(restaurant_id, item_id):
    item_to_delete = session.query(MenuItem).filter_by(id = item_id).one()
    if request.method == 'POST':
        session.delete(item_to_delete)
        session.commit()
        flash("The menu item '%s' was deleted!" % item_to_delete.name)
        return redirect(url_for('restaurant_menu', restaurant_id = restaurant_id))
    return render_template('delete_menu_item.html', restaurant_id = restaurant_id,
                            item_id = item_id, item_to_delete = item_to_delete)


# API endpoint (GET) for entire restaurant menu
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurant_menu_json(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems = [i.serialize for i in items])


# API endpoint (GET) for specific menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/JSON')
def menu_item_json(restaurant_id, item_id):
    item = session.query(MenuItem).filter_by(id = item_id).one()
    return jsonify(MenuItem = item.serialize)

if __name__ == '__main__':
    app.secret_key = "insecure_placeholder"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
