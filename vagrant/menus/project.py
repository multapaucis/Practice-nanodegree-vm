from flask import Flask
from flask import request
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def RestaurantMenu(restaurant_id=1):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    output = ''
    output += "<h1>%s</h1> " % restaurant.name
    for i in items:
        output += "<b>%s</b>" % i.name
        output += " (<a href='/restaurants/%s/" % i.restaurant_id
        output += "%s/edit'>edit</a>)</br>" % i.id
        output += i.price
        output += "</br>"
        output += i.description
        output += '</br></br>'
    output += "<a href='/restaurants/%s/new'>" % restaurant_id
    output += "Add a New Item </a>"
    return output


# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        iname = request.form.get('iname')
        iprice = request.form.get('iprice')
        idescription = request.form.get('descript')

        new_item = MenuItem(restaurant_id=restaurant_id, name=iname, price=iprice, description=idescription)
        session.add(new_item)
        session.commit()

        output = ""
        output += "The New Menu Item, %s, has been added</br></br>" % iname
        output += "<a href='/restaurants/%s/'>" % restaurant_id
        output += "Back to Restaurant Page</a>"
    else:
        output = ""
        output += "<form method='POST' enctype='multipart/form-data' "
        output += "action='/restaurants/%s/new'>" % restaurant_id
        output += "What is the Name of the New Item?</br>"
        output += "<input name='iname' type='text'></br></br>"
        output += "What is the Price of the New Item?</br>"
        output += "<input name='iprice' type='text'></br></br>"
        output += "Please provide a Brief Description of the Item</br>"
        output += "<input name='descript' type='text' size=40></br>"
        output += "</br><input type='submit' value='Submit'> </form>"

    return output

# Task 2: Create route for editMenuItem function here


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        iname = request.form.get('iname', None)
        iprice = request.form.get('iprice', None)
        idescription = request.form.get('descript', None)

        up_item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
        if iname:
            up_item.name = iname
        if iprice:
            up_item.price = iprice
        if idescription:
            up_item.description = idescription
        session.add(up_item)
        session.commit()
        output = ""
        output += "The Menu Item, %s, has been Updated</br></br>" % up_item.name
        output += "<a href='/restaurants/%s/'>" % restaurant_id
        output += "Back to Restaurant Page</a>"

    else:
        item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()

        output = ""
        output += "<h3>Please Leave Any Fields You Don't Wish to Change Blank.</h3>"
        output += "<form method='POST' enctype='multipart/form-data' "
        output += "action='/restaurants/%s/" % restaurant_id
        output += "%s/edit'>" % menu_id
        output += "What is the New Name for the Item?</br>"
        output += "<input name='iname' type='text' value='%s'></br></br>" % item.name
        output += "What is the New Price for the Item?</br>"
        output += "<input name='iprice' type='text' value='%s'></br></br>" % item.price
        output += "Please provide a Brief Description of the Item</br>"
        output += "<input name='descript' type='text' size=40></br>"
        output += "</br><input type='submit' value='Submit'> </form>"

    return output

# Task 3: Create a route for deleteMenuItem function here


def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
