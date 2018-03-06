from flask import Flask
app = Flask(__name__)


@app.route('/')
@app.route('/restaurants')
def Restaurants():
    '''Main Page with all Restaurants listed'''
    return "Main Page with all Restaurants listed"


@app.route('/restaurants/new')
def AddRestaurant():
    '''Page to Add a new Restaurant'''
    return "Page to Add a new Restaurant"


@app.route('/restaurant/<int:restaurant_id>/edit')
def EditRestaurant(restaurant_id):
    '''Page to Edit an existing Restaurant'''
    return "Page to Edit an existing Restaurant"


@app.route('/restaurant/<int:restaurant_id>/delete')
def DeleteRestaurant(restaurant_id):
    '''Page to Delete an existing Restaurant'''
    return "Page to Delete an existing Restaurant"


@app.route('/restaurant/<int:restaurant_id>/menu')
@app.route('/restaurant/<int:restaurant_id>')
def RestaurantMenu(restaurant_id):
    '''Page to Delete an existing Restaurant'''
    return "Main Page with all items for a specific Restaurant listed"


@app.route('/restaurant/<int:restaurant_id>/menu/new')
def AddNewItem(restaurant_id):
    '''Page to Delete an existing Restaurant'''
    return "Page to add an new item to a specific Restaurant's Menu"


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def EditItem(restaurant_id, menu_id):
    '''Page to Delete an existing Restaurant'''
    return "Page to edit an item on a specific Restaurant's Menu"


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def DeleteItem(restaurant_id, menu_id):
    '''Page to Delete an existing Restaurant'''
    return "Page to delete a specific item from a Restaurant's Menu"


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
