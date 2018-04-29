from db_model import Base, Item
from flask import Flask, render_template, json, jsonify, request, redirect, url_for, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///itemCatalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


# Routes/pages
# Main page showing the list of categories and latest items (add item button if logged in)
@app.route('/', methods=['GET', 'POST'])
def catalog():
	categories = session.query(Item).group_by(Item.category).all()
	items = session.query(Item).all()
	if request.method == 'POST':
		return jsonify(items = [i.serialize for i in items])
	else:
		return render_template('catalog.html', categories=categories, items=items)

# Page for adding an item (must be logged in)
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newItem():
	if request.method == 'GET':
		return render_template('newitem.html')
	if request.method == 'POST':
		newItem = Item(name = request.form['name'], category = request.form['category'], description = request.form['description'])
		session.add(newItem)
		session.commit()
		return redirect(url_for('catalog')) #redirect(url_for('itemInfo', category=newItem.category, item=newItem))

# Page for viewing all items within a category
@app.route('/catalog/<string:category>/items/', methods=['GET'])
def categoryList(category):
	return render_template('categorylist.html')

# Page for viewing a specific item (with edit and delete items if logged in)
@app.route('/catalog/<string:category>/<string:item>/', methods=['GET'])
def itemInfo(category, item):
	item = session.query(Item).filter_by(id = item.id).one()
	return render_template('iteminfo.html', item=item)

# Page to edit an item (must be logged in)
@app.route('/catalog/<string:item>/edit/', methods=['GET', 'PUT'])
def editItem(item):
	return render_template('edititem.html')

# Page to confirming deletion of an item (must be logged in)
@app.route('/catalog/<string:item>/delete', methods=['GET', 'POST'])
def deleteItem(item):
	return render_template('deleteitem.html')


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=8000)