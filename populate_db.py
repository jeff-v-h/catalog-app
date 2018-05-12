from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_model import Base, User, Item

engine = create_engine('sqlite:///itemCatalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def addItems():
    session.add(Item(
        name="Ankle Brace", category="basketball", 
        description="A bace to provide extra stability for the ankle"))
    session.add(Item(
        name="Towel", category="basketball", 
        description="Wipe away sweat to keep yourself dry"))
    session.add(Item(
        name="Hyperdunks", category="basketball", description="Shoes by Nike"))
    session.add(Item(
        name="Shin Pads", category="soccer", 
        description="Guard the shins, they get kicked often."))
    session.add(Item(
        name="World Cup Ball", category="soccer", 
        description="2018 World Cup official ball"))
    session.add(Item(
        name="Head Racket", category="tennis", 
        description="Titanium racket by Head"))
    session.add(Item(
        name="Tennis ball x4", category="tennis", 
        description="4x tennis balls"))
    session.add(Item(
        name="Endeavour Snowboard", category="snowboarding", 
        description="All round board suitable for beginners"))
    session.add(Item(
        name="Gloves Waterproof", category="snowboarding", 
        description="Thinsulate waterproof gloves suitable for up to \
        -20 degrees")
    session.add(Item(
        name="Speedo Goggles", category="swimming", 
        description="Protect those eyes. Made by Speedo"))
    session.add(Item(
        name="Speedo Trunks", category="swimming", 
        description="Cover the lower half of your body for competitive races"))
    session.add(Item(
        name="Rugby Union Ball", category="rugby", 
        description="Ball used in the Rugby World Cup"))
    session.add(Item(
        name="Rugby tee", category="rugby", 
        description="Tee to practice your goal kicks"))
    session.commit()
    print "Item database populated."

brace = session.query(Item).filter_by(name="Ankle Brace").first()
if item_brace is None:
    addItems()
