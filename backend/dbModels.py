from dotenv import dotenv_values
from flask import Flask
from datetime import datetime
import os
from flask import current_app, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, Boolean, create_engine
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
db = SQLAlchemy()

# Creating Sessions for multi threading
engine = create_engine(dotenv_values(".env.cfg")["DB_FULL_URI"])
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# reservation_table = Table('reservation_table', Base.metadata,
#     Column('account_id', Integer, ForeignKey('account.id')),
#     Column('reservation_id', Integer, ForeignKey('reservation.id'))
# )

# favTable = Table('favTable',
#     Base.metadata,
#     Column('account_id', Integer, ForeignKey('account.id')),
#     Column('local_id', Integer, ForeignKey('lokal.id'))
# )

class Account(db.Model):
    __tablename__ = 'account'
    _id = Column("id", Integer, primary_key=True)
    name = Column("name", String, nullable=False)
    street = Column("street", String)
    plz = Column("plz", String(5))
    #favorites = relationship('Lokal', secondary=favTable, backref='followers')
    # ownerLokal = relationship('Lokal', back_populates="account", uselist=False)
    # reservation_id = Column(Integer, ForeignKey('reservation.id'))
    reservation = relationship("Reservation")
    ownesLokal = relationship("Lokal")
    def __init__(self, name, street, plz):
        self.name = name
        self.street = street
        self.plz = plz
    def __repr__(self):
        return f"{self.name} - Age:{self.age}"

class Reservation(db.Model):
    __tablename__ = 'reservation'
    _id = Column("id", Integer, primary_key=True)
    datetime = Column(DateTime, default = datetime.utcnow)
    accepted = Column(Boolean, default = False)
    reservedBy = Column(Integer, ForeignKey("account.id"))
    reservedLocal = Column(Integer, ForeignKey("lokal.id"))

class Lokal(db.Model):
    __tablename__ = 'lokal'
    _id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    owner = Column("owner", Integer, ForeignKey("account.id"))
    reservation = relationship("Reservation")
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner

def addObj(obj):
    session = Session()
    try: 
        session.add(obj)
        session.commit()
    except Exception as e:
        print(e)
        return make_response("ERROR accured. Couldn't create Database Object.")
