from db_model import Base, Item
from flask import (
    Flask, render_template, json, jsonify, request, redirect,
    url_for, flash, g)
from flask import session as login_session
import random, string
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///itemCatalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


# Create a state token to prevent request forgery
# Store it in the session for later validation
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# JSON API endpoints
# JSON API for all items in the catalog
@app.route('/catalog/JSON')
def catalogJSON():
    items = session.query(Item).all()
    return jsonify(items=[i.serialize for i in items])


# JSON API for all items in a specific category
@app.route('/catalog/<string:category>/JSON')
def categoryJSON(category):
    items_in_category = session.query(Item).filter_by(category=category).all()
    return jsonify(items_in_category=[i.serialize for i in items_in_category])


# JSON API for a specific item.
# Both name and id required in case there are items of same name
@app.route('/catalog/<string:item_name>/<int:item_id>/JSON')
def itemJSON(item_name, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item=item.serialize)


# Routes/pages
# Main page showing the list of categories and latest items
@app.route('/', methods=['GET', 'POST'])
@app.route('/catalog/', methods=['GET', 'POST'])
def catalog():
    items_group_by_category = session.query(Item).group_by(Item.category).all()
    items = session.query(Item).all()
    if request.method == 'POST':
        return jsonify(items=[i.serialize for i in items])
    else:
        return render_template(
            'catalog.html',
            items_grouped_by_category=items_group_by_category, items=items)


# Page for adding an item (must be logged in)
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newItem():
    if request.method == 'GET':
        return render_template('newitem.html')
    if request.method == 'POST':
        if request.form['name'] and request.form['description']:
            newItem = Item(
                name=request.form['name'],
                category=request.form['category'],
                description=request.form['description'])
            session.add(newItem)
            session.commit()
            flash("New item created: " + newItem.name)
            return redirect(url_for(
                'itemInfo', category=newItem.category,
                item_name=newItem.name, item_id=newItem.id))
        else:
            print "All fields required."
            flash("ERROR: All fields need to be populated.")
            return render_template('newitem.html')


# Page for viewing all items within a category
@app.route('/catalog/<string:category>/items/', methods=['GET'])
def categoryList(category):
    items_group_by_category = session.query(Item).group_by(Item.category).all()
    items_in_category = session.query(Item).filter_by(category=category).all()
    return render_template(
        'categorylist.html',
        items_grouped_by_category=items_group_by_category,
        category=category,
        items=items_in_category)


# Page for viewing a specific item (with edit and delete items if logged in)
@app.route(
    '/catalog/<string:category>/<string:item_name>/<int:item_id>',
    methods=['GET'])
def itemInfo(category, item_name, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('iteminfo.html', item=item)


# Page to edit an item (must be logged in)
@app.route(
    '/catalog/<string:item_name>/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(item_name, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'GET':
        return render_template('edititem.html', item=item)
    if request.method == 'POST':
        if request.form['name'] and request.form['description']:
            item.name = request.form['name']
            item.description = request.form['description']
            item.category = request.form['category']
            session.add(item)
            session.commit()
            flash(item.name + " edited successfully.")
            return redirect(url_for(
                'itemInfo', category=item.category,
                item_name=item.name, item_id=item.id))
        else:
            print "fields for name and description required."
            flash("ERROR: All fields need to be populated.")
            return redirect(url_for(
                'editItem', item_name=item.name, item_id=item.id))


# Page to confirming deletion of an item (must be logged in)
@app.route(
    '/catalog/<string:item_name>/<int:item_id>/delete',
    methods=['GET', 'POST'])
def deleteItem(item_name, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'GET':
        return render_template('deleteitem.html', item=item)
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash(item.name + " deleted successfully.")
        return redirect(url_for('categoryList', category=item.category))

if __name__ == '__main__':
    app.secret_key = 'catalog_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
