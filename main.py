from flask import Flask,redirect,render_template,url_for,jsonify,request
app=Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem

engine=create_engine('sqlite:///restaurantmenu.db',connect_args={'check_same_thread': False})
Base.metadata.bind=engine
DBsession=sessionmaker(bind=engine)
session=DBsession()

### ---- show the Restaurants/homepage ---- ###

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurantList=session.query(Restaurant).all()
    return render_template('restaurants.html',restaurants=restaurantList)

### ---- Create a new Restaurant ---- ##

@app.route('/restaurant/new', methods=['GET','POST'])
def newRestaurant():
    if request.method=="POST":
        newRestItem=Restaurant(name=request.form['name'])
        session.add(newRestItem)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

### ---- Edit a Restaurant ---- ##        

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
    editRestItem=session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method=="POST":
       editRestItem.name=request.form['name']
       session.add(editRestItem)
       session.commit()
       return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html',restaurant_id=restaurant_id,r=editRestItem)

### ---- Delete a  Restaurant ---- ##

@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    delRestItem=session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method=="POST":
        session.delete(delRestItem)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html',restaurant=delRestItem)

### ---- Display menu of a restaurant ---- ##

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    items=session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return render_template("menu.html",restaurant=restaurant,items=items)

### ---- Creant a new menu item ---- ##

@app.route('/restaurant/<int:restaurant_id>/menu/new',methods=["GET","POST"])
def newMenuItem(restaurant_id):
    if request.method=='POST':
        newItem=MenuItem(name=request.form['name'],
                         description=request.form['description'],
                         course=request.form['course'],
                         price=request.form['price'],
                         restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showMenu',restaurant_id=restaurant_id))
    else :
        return render_template('newMenuItem.html',restaurant_id=restaurant_id)

### ---- Edit a menu item ---- ##        

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',methods=["GET","POST"])
def editMenuItem(restaurant_id,menu_id):
    editItem=session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method=="POST":
        if request.form['name']:
            editItem.name=request.form['name']
        if request.form['description']:
            editItem.description=request.form['description']
        if request.form['price']:
            editItem.price=request.form['price']
        if request.form['course']:
            editItem.course=request.form['course']
        session.add(editItem)
        session.commit()
        return redirect(url_for('showMenu',restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html',restaurant_id=restaurant_id,i=editItem)

### ---- Delete a menu item ---- ##        

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',methods=["GET","POST"])
def deleteMenuItem(restaurant_id,menu_id):
    itemToDelete=session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method=='POST':
       session.delete(itemToDelete)
       session.commit()
       return redirect(url_for('showMenu',restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html',i=itemToDelete)

### ---- Adding API endpoints (GET Requests) ---###

@app.route('/restaurants/JSON')
def showRestaurantsJSON():
    restaurantList=session.query(Restaurant).all()
    return jsonify(Restaurants=[r.serialize for r in restaurantList])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def showMenuJSON(restaurant_id):
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    items=session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def showMenuItemJSON(restaurant_id,menu_id):
    menuItem=session.query(MenuItem).filter_by(id=menu_id,restaurant_id=restaurant_id).one()
    return jsonify(MenuItem=menuItem.serialize)

if __name__=="__main__":
    app.run('0.0.0.0',port=5000,debug=True)