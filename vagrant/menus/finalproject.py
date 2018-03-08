from flask import Flask
from flask import render_template, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants')
def restaurants():
    '''Main Page with all Restaurants listed'''
    restaurantList = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurantList)


@app.route('/restaurants/new', methods=['GET', 'POST'])
def addRestaurant():
    '''Page to Add a new Restaurant'''
    return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    '''Page to Edit an existing Restaurant'''
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('editRestaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    '''Page to Delete an existing Restaurant'''
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('deleteRestaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu')
@app.route('/restaurant/<int:restaurant_id>')
def restaurantMenu(restaurant_id):
    '''Page to Display all Items for a Specific Restaurant'''
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    '''Page to add an item to a specific Restaurant'''
    return render_template('newMenuItem.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    '''Page to edit a specific item from a Restaurant'''
    item = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id, id=menu_id).one()
    return render_template('editMenuItem.html', item=item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    '''Page to Delete a specific item from a Restaurant'''
    item = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id, id=menu_id).one()
    return render_template('deleteMenuItem.html', item=item)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
