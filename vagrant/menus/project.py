from flask import Flask
from flask import request, redirect, url_for
from flask import render_template, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Main Restaurant Page Displaying all Menu items with price & Description
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def RestaurantMenu(restaurant_id=1):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


# Provides Forms to create ne w menu Item
@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        iname = request.form.get('iname')
        iprice = request.form.get('iprice')
        idescription = request.form.get('descript')
        new_item = MenuItem(restaurant_id=restaurant_id, name=iname,
                            price=iprice, description=idescription)
        session.add(new_item)
        session.commit()
        flash('The New Item has been Added!')
        return redirect(url_for('RestaurantMenu', restaurant_id=restaurant_id))

    else:
        return render_template('newitem.html', restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
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
        flash("The Item has been Updated")
        return redirect(url_for('RestaurantMenu', restaurant_id=restaurant_id))

    else:
        item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id,
                                                 id=menu_id).one()

        return render_template('edit_item.html', item=item)

# Task 3: Create a route for deleteMenuItem function here


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':

        rest = session.query(MenuItem).filter_by(
                restaurant_id=restaurant_id, id=menu_id).one()
        session.delete(rest)
        session.commit()
        flash("The requested item has been deleted")
        return redirect(url_for('RestaurantMenu', restaurant_id=restaurant_id))

    else:
        item = session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id, id=menu_id).one()

        return render_template('delete_item.html', item=item)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
