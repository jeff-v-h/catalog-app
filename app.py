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
# Main page
@app.route('/')
def ():
	return

# Page for viewing all items within a category
@app.route('/')
def ():
	return

# Page for viewing a specific item
@app.route('/')
def ():
	return

# Page to edit an item
@app.route('/')
def ():
	return

# Page to confirming deletion of an item
@app.route('/')
def ():
	return
