from flask import Flask,redirect,render_template,url_for,jsonify,request
app=Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem

engine=create_engine('sqlite:///restaurantmenu.db',connect_args={'check_same_thread': False})
Base.metadata.bind=engine
DBsession=sessionmaker(bind=engine)
session=DBsession()

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurantList=session.query(Restaurant).all()
    return render_template('restaurants.html',restaurants=restaurantList)

@app.route('/restaurant/new', methods=['GET','POST'])
def newRestaurant():
    if request.method=="POST":
        newRestItem=Restaurant(name=request.form['name'])
        session.add(newRestItem)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

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


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    delRestItem=session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method=="POST":
        session.delete(delRestItem)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html',restaurant=delRestItem)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    items=session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return render_template("menu.html",restaurant=restaurant,items=items)

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

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id,menu_id):
    return "This page is for editing menu item %s" %menu_id

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id,menu_id):
    return "This page is for deleting menu item %s" %menu_id

if __name__=="__main__":
    app.run('0.0.0.0',port=5000,debug=True)