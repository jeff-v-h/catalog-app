from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_model import Base, User, Item
from datetime import datetime

engine = create_engine('sqlite:///itemCatalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def addUser():
    session.add(User(id=1, username="Jeffrey Huang", email="jh0791@gmail.com"))
    session.commit()
    print "User 1 added."


def addItems():
    session.add(Item(
        name="Ankle Brace", category="basketball", user_id=1,
        description="A bace to provide extra stability for the ankle",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow(),))
    session.add(Item(
        name="Towel", category="basketball", user_id=1,
        description="Wipe away sweat to keep yourself dry",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="Hyperdunks", category="basketball", description="Shoes by Nike",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow(),
        user_id=1))
    session.add(Item(
        name="Shin Pads", category="soccer", user_id=1,
        description="Guard the shins, they get kicked often.",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="World Cup Ball", category="soccer", user_id=1,
        description="2018 World Cup official ball",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="Head Racket", category="tennis", user_id=1,
        description="Titanium racket by Head",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="Tennis ball x4", category="tennis", user_id=1,
        description="4x tennis balls",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="Endeavour Snowboard", category="snowboarding", user_id=1,
        description="All round board suitable for beginners",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="Gloves Waterproof", category="snowboarding", user_id=1,
        description="Thinsulate waterproof gloves suitable for up to -20 deg",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="Speedo Goggles", category="swimming", user_id=1,
        description="Protect those eyes. Made by Speedo",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="Speedo Trunks", category="swimming", user_id=1,
        description="Cover the lower half of your body for competitive races",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="Rugby Union Ball", category="rugby", user_id=1,
        description="Ball used in the Rugby World Cup",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="Rugby tee", category="rugby", user_id=1,
        description="Tee to practice your goal kicks",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.commit()
    print "Item database populated."

user = session.query(Item).filter_by(id=1).first()
if user is None:
    addUser()

brace = session.query(Item).filter_by(name="Ankle Brace").first()
if brace is None:
    addItems()
