# Sports Catalog App

## Application Description

A web application to display items in a catalog. It stores information about items from various categories. The items can be edited or deleted but this may require the user to login. Certain items can only be changed depending on user authentication and authorisation.



## Requirements

### Required Libraries and Dependencies

- Python2
- Flask
- SQLAlchemy
- Vagrant
- VirtualBox

### Project Contents

- app.py file runs all the main routeing webpages, JSON endpoints, authentication and authorization
- db_model.py file creates the database tables and columns
- populate_db.py file adds a user and several items in to the database if they are not already there
- static folder includes styles.css file which has the styling for all current webpages
- templates folder includes all html templates for each page. Most of the pages extend from baselayout.html



## Installation

### Google OAuth
This repository includes the client_secrets.json file along with the clientID and client_secret already implemented into the files.
If your own google account is required, you will need to create a google account and go to https://console.developers.google.com to create a project and to obtain your own google OAuth2.0 clientID and secret. You may also need to add <http://localhost:8000> as an Authorized JavaScript origin along with <http://localhost:8000/gconnect> and <http://localhost:8000/login> as Authorized redirect URIs.
If you have your own clientID, replace the current one in login.html file

### Dependencies
requirements.txt is available. 
Run `pip install -r requirements.txt` if you have any missing dependencies to help your app run smoothly



## Operating Instructions

### How to Setup Environment

1. Download and unzip the project files or `git clone` this repository
2. Navigate to the directory where the files are downloaded to
3. Launch vagrant environment with `vagrant up` and then login with `vagrant ssh`
4. `cd /vagrant` and then navigate to the folder within the vagrant environment

### How to Run and Populate the Database

5. It may be necessary to populate the database using `python populate_db.py` You can try this step even if the database (itemCatalog.db) is already there since duplicates will not be made. Running populate_db.py will automatically setup the database before populating.

### How to Run the Application

6. Execute the program with `python app.py` in your terminal while inside the root directory where app.py file is
7. Using your preferred web browser, visit <http://localhost:8000/> to get started.
