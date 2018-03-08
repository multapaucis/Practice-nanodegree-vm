from flask import Flask
from flask import render_template, redirect, url_for, request, flash
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
    if request.method == 'POST':
        new_name = request.form.get('rname')
        new_restaurant = Restaurant(name=new_name)
        session.add(new_restaurant)
        session.commit()
        flash("{} has been added!".format(new_name))
        return redirect(url_for('restaurants'))
    else:
        return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    '''Page to Edit an existing Restaurant'''
    if request.method == 'POST':
        new_name = request.form.get('rname', None)
        up_rest = session.query(Restaurant).filter_by(id=restaurant_id).one()
        if new_name:
            up_rest.name = new_name
        session.add(up_rest)
        session.commit()
        return redirect(url_for('restaurants'))
    else:
        restaurant = session.query(Restaurant).filter_by(
            id=restaurant_id).one()
        return render_template('editRestaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    '''Page to Delete an existing Restaurant'''
    if request.method == 'POST':
        del_rest = session.query(Restaurant).filter_by(id=restaurant_id).one()
        session.delete(del_rest)
        session.commit()
        return redirect(url_for('restaurants'))
    else:
        restaurant = session.query(Restaurant).filter_by(
            id=restaurant_id).one()
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
    if request.method == 'POST':
        iname = request.form.get('iname')
        iprice = request.form.get('iprice')
        idescription = request.form.get('descript')
        new_item = MenuItem(restaurant_id=restaurant_id, name=iname,
                            price=iprice, description=idescription)
        session.add(new_item)
        session.commit()
        flash('{} has been Added!'.format(iname))
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    '''Page to edit a specific item from a Restaurant'''
    if request.method == 'POST':
        iname = request.form.get('iname', None)
        iprice = request.form.get('iprice', None)
        idescription = request.form.get('descript', None)

        up_item = session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id, id=menu_id).one()
        if iname:
            up_item.name = iname
        if iprice:
            up_item.price = iprice
        if idescription:
            up_item.description = idescription
        session.add(up_item)
        session.commit()
        flash("{} has been Updated".format(iname))
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    else:
        item = session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id, id=menu_id).one()
        return render_template('editMenuItem.html', item=item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    '''Page to Delete a specific item from a Restaurant'''
    if request.method == 'POST':
        del_item = session.query(MenuItem).filter_by(
                restaurant_id=restaurant_id, id=menu_id).one()
        session.delete(del_item)
        session.commit()
        flash("{} has been deleted".format(del_item.name))
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        item = session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id, id=menu_id).one()
        return render_template('deleteMenuItem.html', item=item)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
