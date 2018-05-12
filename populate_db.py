from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_model import Base, User, Item
from datetime import datetime

engine = create_engine('sqlite:///itemCatalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def addItems():
    session.add(Item(
        name="Ankle Brace", category="basketball", 
        description="A bace to provide extra stability for the ankle",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="Towel", category="basketball", 
        description="Wipe away sweat to keep yourself dry",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="Hyperdunks", category="basketball", description="Shoes by Nike",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="Shin Pads", category="soccer", 
        description="Guard the shins, they get kicked often.",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="World Cup Ball", category="soccer", 
        description="2018 World Cup official ball",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="Head Racket", category="tennis", 
        description="Titanium racket by Head",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="Tennis ball x4", category="tennis", 
        description="4x tennis balls",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="Endeavour Snowboard", category="snowboarding", 
        description="All round board suitable for beginners",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="Gloves Waterproof", category="snowboarding", 
        description="Thinsulate waterproof gloves suitable for up to \
        -20 degrees",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="Speedo Goggles", category="swimming", 
        description="Protect those eyes. Made by Speedo",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="Speedo Trunks", category="swimming", 
        description="Cover the lower half of your body for competitive races",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="Rugby Union Ball", category="rugby", 
        description="Ball used in the Rugby World Cup",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.add(Item(
        name="Rugby tee", category="rugby", 
        description="Tee to practice your goal kicks",
        created_date=datetime.utcnow(), modified_date=datetime.utcnow()))
    session.commit()
    print "Item database populated."

brace = session.query(Item).filter_by(name="Ankle Brace").first()
if brace is None:
    addItems()
