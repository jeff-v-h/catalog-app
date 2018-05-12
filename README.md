# Sports Catalog App

## Application Description

A web application to display items in a catalog. It stores information about items from various categories. The items can be edited or deleted but this may require the user to login. Certain items can only be changed depending on user authentication and authorisation.

## Requirements

- Python2
- Flask
- SQLAlchemy
- Vagrant
- VirtualBox

## How to Run the Application

1. Download and unzip the project files or `git clone` this repository
2. Navigate to the directory where the files are downloaded to
3. Launch vagrant environment with `vagrant up` and then login with `vagrant ssh`
4. `cd /vagrant` and then navigate to the folder within the vagrant environment
5. It may be necessary to populate the database using `python populate_db.py` You can try this step even if the database is there. Duplicates will not be made.
6. Execute the program with `python app.py`
7. Using your preferred web browser, visit http://localhost:8000/
