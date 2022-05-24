from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
db = SQLAlchemy()

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
    age = Column("age", Integer)
    #favorites = relationship('Lokal', secondary=favTable, backref='followers')
    # ownerLokal = relationship('Lokal', back_populates="account", uselist=False)
    # reservation_id = Column(Integer, ForeignKey('reservation.id'))
    # reservation = relationship("Reservation")
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __repr__(self):
        return f"{self.name} - Age:{self.age}"

class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True)
    personNumber = Column(Integer)
    datetime = Column(DateTime, default = datetime.utcnow)
    accepted = Column(Boolean, default = False)

class Lokal(db.Model):
    __tablename__ = 'lokal'
    id = Column(Integer, primary_key=True)
    # account = relationship("Account")
    # ownedBy = relationship("Account", back_populates="lokal")

