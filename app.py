from db_model import Item
from flask import Flask, jsonify, request, url_for, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///itemCatalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


# Routes/pages
# Main page showing the list of categories and latest items
@app.route('/')
def catalog():
	return "This is the main page."

# Page for viewing all items within a category
@app.route('/catalog/<string:category>/items/')
def categoryList(category):
	return "This is a category page."

# Page for viewing a specific item
@app.route('/catalog/<string:category>/<string:item>/')
def itemInfo(category, item):
	return "This is a page for an item."

# Page to edit an item
@app.route('/catalog/<string:item>/edit/')
def editItem(item):
	return "This is the page to edit an item."

# Page to confirming deletion of an item
@app.route('/catalog/<string:item>/delete')
def deleteItem(item):
	return "This is the page to delete an item."


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=8000)