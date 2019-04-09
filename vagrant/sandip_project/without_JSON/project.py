from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#List of all the restaurants available
@app.route('/')
def restaurantList():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/new', methods=['GET','POST'])
def addNewRestaurant():
	if request.method == 'POST':
		newRestaurant = Restaurant(id=request.form['id'], name=request.form['name'])
		session.add(newRestaurant)
		session.commit()

		return redirect(url_for('restaurantList'))
	else:
		return render_template('addnewrestaurant.html')

#Delete any of the restaurant
@app.route('/restaurant/<int:restaurant_id>/del', methods=['GET','POST'])
def restaurantDelete(restaurant_id):
	restaurant_ed = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		session.delete(restaurant_ed)
		session.commit()

		return redirect(url_for('restaurantList'))
	else:
		return render_template('deleterestaurant.html', restaurant_id=restaurant_id, restaurant = restaurant_ed )

#Edit any restaurant
@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
	restaurant_edit = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			restaurant_edit.name = request.form['name']
		session.add(restaurant_edit)
		session.commit()

		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('editrestaurant.html', restaurant_id=restaurant_id, restaurant = restaurant_edit)



#Details of the complete Menu of the selected Restaurant
@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
	return render_template('menu.html', restaurant=restaurant, items=items, restaurant_id=restaurant_id)


#If any new Menu should be added in the Restaurant Menu list
@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def addMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], restaurant_id=restaurant_id)
		session.add(newItem)
		flash("New Menu Item has been created successfully")
		session.commit()
		
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id=restaurant_id)


#If any of the fields of the Menu needs to be Edited
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id=menu_id).one()

	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['description']:
			editedItem.description = request.form['description']
		if request.form['price']:
			editedItem.price = request.form['price']
		if request.form['course']:
			editedItem.course = request.form['course']

		session.add(editedItem)
		session.commit()
		flash("This item has been edited successfully - %s" %editedItem.name)
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)
	
#If any existing menu needs to be deleted
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()

	if request.method == 'POST':
		session.delete(deletedItem)
		session.commit()
		flash("This item has been deleted successfully - %s" %deletedItem.name)
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('deleteMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=deletedItem)
	

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
    	app.debug = True
    	app.run(host='0.0.0.0', port=5000)
