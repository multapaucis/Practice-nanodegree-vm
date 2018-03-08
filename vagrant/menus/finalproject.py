from flask import Flask
from flask import render_template, redirect, url_for, request, flash, jsonify
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


@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    '''Page to Edit an existing Restaurant'''
    if request.method == 'POST':
        new_name = request.form.get('rname', None)
        up_rest = session.query(Restaurant).filter_by(id=restaurant_id).one()
        if new_name:
            up_rest.name = new_name
        session.add(up_rest)
        session.commit()
        flash("{} has been updated!".format(new_name))
        return redirect(url_for('restaurants'))
    else:
        restaurant = session.query(Restaurant).filter_by(
            id=restaurant_id).one()
        return render_template('editRestaurant.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    '''Page to Delete an existing Restaurant'''
    if request.method == 'POST':
        del_rest = session.query(Restaurant).filter_by(id=restaurant_id).one()
        session.delete(del_rest)
        session.commit()
        flash("{} has been removed".format(del_rest.name))
        return redirect(url_for('restaurants'))
    else:
        restaurant = session.query(Restaurant).filter_by(
            id=restaurant_id).one()
        return render_template('deleteRestaurant.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/menu')
@app.route('/restaurants/<int:restaurant_id>')
def restaurantMenu(restaurant_id):
    '''Page to Display all Items for a Specific Restaurant'''
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route(
    '/restaurants/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    '''Page to add an item to a specific Restaurant'''
    if request.method == 'POST':
        iname = request.form.get('iname')
        iprice = request.form.get('iprice')
        icourse = request.form.get('icourse')
        idescription = request.form.get('descript')
        new_item = MenuItem(restaurant_id=restaurant_id, name=iname,
                            price=iprice, description=idescription,
                            course=icourse)
        session.add(new_item)
        session.commit()
        flash('{} has been Added!'.format(iname))
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    '''Page to edit a specific item from a Restaurant'''
    if request.method == 'POST':
        iname = request.form.get('iname', None)
        iprice = request.form.get('iprice', None)
        idescription = request.form.get('descript', None)
        icourse = request.form.get('course', None)

        up_item = session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id, id=menu_id).one()
        if iname:
            up_item.name = iname
        if iprice:
            up_item.price = iprice
        if idescription:
            up_item.description = idescription
        if icourse:
            up_item.course = icourse

        session.add(up_item)
        session.commit()
        flash("{} has been Updated".format(iname))
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    else:
        item = session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id, id=menu_id).one()
        return render_template('editMenuItem.html', item=item)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete',
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


@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[r.serialize for r in restaurants])


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant.id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id, id=menu_id).one()
    return jsonify(MenuItem=item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
