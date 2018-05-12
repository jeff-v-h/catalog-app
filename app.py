from db_model import Base, User, Item
from flask import (
    Flask, render_template, json, jsonify, request, redirect,
    url_for, flash, g, make_response)
from flask import session as login_session
import random, string
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
from datetime import datetime


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

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


# Method to connect to google for user to login with their google account
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # confirm client token sent to server matches token server sent to client
    if request.args.get('state') != login_session['state']:
        return jsonify('Invalid state.'), 401

    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        return jsonify('Failed to upgrade the authorization code.'), 401

    #Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
        % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        return jsonify(result.get('error')), 500
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        return jsonify("Token's user ID doesn't match given user ID."), 401
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        print "Token's client ID does not match app's."
        return jsonify("Token's client ID does not match app's."), 401

    # Check to see if the user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        return jsonify('Current user is already connected.'), 200

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    # store info from data into login session
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # if user does not exist in database, add as a new user
    user = session.query(User).filter_by(email=login_session['email']).first()
    login_session['user_id'] = user.id
    if user is None:
        createUser(login_session)

    # return a welcome page including info stored from user's data
    # also return flash message to let them know their login was successful
    output = ''
    output = '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += '"style = "width: 300px; height: 300px; border-radius: 150px; "'
    output += '-webkit-border-radius: 150px; -moz-border-radius: 150px;">'
    flash("You are now logged in as %s" % login_session['username'])
    return output


# Disconnect - Revoke a current user's token and reset their login_session
@app.route("/gdisconnect")
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session['access_token']
    if access_token is None:
        print 'Access token is None'
        return jsonify('Current user not connected.'), 401

    # Execute HTTP GET request to revoke current token
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s' 
        % access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's session.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']

        flash('Successfully logged out')
        return redirect(url_for('showLogin'))
    else:
        # For whatever reason, the given token was invalid.
        return jsonify('Failed to revoke token for given user.'), 400


# Helper function: Create a new user with login session details
def createUser(login_session):
    newUser = User(
        username=login_session['username'], 
        email=login_session['email'], 
        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    print "User created with id "
    print user.id


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
    items_latest = session.query(Item).order_by(
        Item.modified_date.desc()).limit(10).all()
    if request.method == 'POST':
        return jsonify(items=[i.serialize for i in items])
    else:
        return render_template(
            'catalog.html',
            items_grouped_by_category=items_group_by_category,
            items_latest=items_latest)


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
                description=request.form['description'],
                created_date=datetime.utcnow(),
                modified_date=datetime.utcnow(),
                user_id=login_session['user_id'])
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
    # Redirect to login page if there is not logged in user
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))

    item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'GET':
        return render_template('edititem.html', item=item)

    if request.method == 'POST':
        if request.form['name'] and request.form['description']:
            item.name = request.form['name']
            item.description = request.form['description']
            item.category = request.form['category']
            item.modified_date = datetime.utcnow()
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
    # Redirect to login page if there is not logged in user
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))

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
