from flask import Flask, render_template, request, url_for, redirect, jsonify,  flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# A test project
# specifiy db engine
engine = create_engine('sqlite:///restaurantmenu.db')
# bind base class to db translate class to table
Base.metadata.bind = engine
# create session makeer object for sending data on session
DBSession = sessionmaker(bind = engine)
session = DBSession()

app = Flask(__name__)

# comments below 
# bug1 html placeholder for edit radio button on edit menu
# json hack

@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/JSON/')
def showRestaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in restaurants])
    #return jsonify(Restaurants=[{"id" : 1, "name" : "noe"},{"id" : 2, "name" : "sdf"},{"id" : 3, "name" : "rrr"}])


@app.route('/restaurant/new/', methods=['GET','POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash('New Restaurant Created')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newrestaurant.html') 

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET','POST'])
def editRestaurant(restaurant_id):
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
        session.add(editedRestaurant)
        session.commit()
        flash('Restaurant Successfully Edited')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editrestaurant.html', restaurant_id = restaurant_id, restaurant = editedRestaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/',methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    deletedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(deletedRestaurant)
        session.commit()
        flash('Restaurant Successfully Deleted')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleterestaurant.html', restaurant = deletedRestaurant)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()    
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
def showMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()    
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/new/',methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'].title(),restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash('New Menu Item Created')
        return redirect(url_for('showMenu',restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/',methods=['GET','POST'])
def editMenuItem(restaurant_id,menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:            
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course'].title()
        session.add(editedItem)
        session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('showMenu',restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def showMenuItemJSON(restaurant_id,menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    food = item.serialize
    #food = {"ham" : 1, "egg" : "yes", "spam" : "no" }
    return jsonify(MenuItem=food)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/',methods=['GET','POST'])
def deleteMenuItem(restaurant_id,menu_id):
    deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showMenu',restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html',restaurant_id = restaurant_id, menu_id = menu_id, item = deletedItem)

if __name__ == '__main__':
    app.secret_key = 'super_key_encode'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
