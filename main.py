from flask import Flask,redirect,render_template,url_for,jsonify
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
    return "This page will show all my restaurants"

@app.route('/restaurant/new')
def newRestaurant():
    return "This page will be for making new restaurant"

@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    return "This page will be for editing restaurant %s" %restaurant_id

@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    return "This page will be for deleting restaurant %s" %restaurant_id

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    return "This page is the menu for restaurant %s" %restaurant_id

@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    return "This page is for making a new menu item for restaurant %s" %restaurant_id

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id,menu_id):
    return "This page is for editing menu item %s" %menu_id

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id,menu_id):
    return "This page is for deleting menu item %s" %menu_id

if __name__=="__main__":
    app.run('0.0.0.0',port=5000,debug=True)