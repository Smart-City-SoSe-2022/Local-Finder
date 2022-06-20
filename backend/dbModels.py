from flask import make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, create_engine
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
db = SQLAlchemy()

favTable = db.Table( 'favTable',
    Column('account_id', ForeignKey('account.id')),
    Column('lokal_id', ForeignKey('lokal.id'))
)

typeTable = db.Table( 'typeTable',
    Column('lokal_id', ForeignKey('lokal.id')),
    Column('lokal_type', ForeignKey('lokaltype.type'))
)

class Account(db.Model):
    __tablename__ = 'account'
    _id = Column("id", Integer, primary_key=True)
    name = Column("name", String, nullable=False)
    street = Column("street", String)
    plz = Column("plz", String(5))
    
    favorites = relationship('Lokal', secondary=favTable, back_populates='faved_by')
    reservation = relationship("Reservation")
    def __init__(self, name, street, plz):
        self.name = name
        self.street = street
        self.plz = plz
    def __repr__(self):
        return f"{self.name}"

class Reservation(db.Model):
    __tablename__ = 'reservation'
    _id = Column("id", Integer, primary_key=True)
    datetime = Column(String)
    accepted = Column(Boolean, default = False)
    reservedBy = Column(Integer, ForeignKey("account.id"))
    reservedLocal = Column(Integer, ForeignKey("lokal.id"))
    def __init__(self, datetime, acc, lokal):
        self.datetime = datetime
        self.reservedBy = acc
        self.reservedLocal = lokal

class Lokal(db.Model):
    __tablename__ = 'lokal'
    _id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    owner = Column("owner", Integer, ForeignKey("account.id"))
    address = Column('address', String)
    plz = Column('plz', String)
    city = Column('city', String)
    reservation = relationship("Reservation")
    faved_by = relationship('Account', secondary=favTable, back_populates='favorites')
    types = relationship('LokalType',  secondary=typeTable, back_populates='lokals')
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner

class LokalType(db.Model):
    __tablename__ = "lokaltype"
    _type = Column("type", String, primary_key=True)
    lokals = relationship('Lokal',  secondary=typeTable, back_populates='types')


def addObj(obj):
    try:
        db.session.add(obj)
        db.session.commit()
    except Exception as e:
        print(e)
        return make_response("ERROR accured. Couldn't create Database Object.")

def delObj(obj):
    try: 
        db.session.delete(obj)
        db.session.commit()
    except Exception as e:
        print(e)
        return make_response("ERROR accured. Couldn't create Database Object.")