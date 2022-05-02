from flask import Flask
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class Day(DB.Model):
    """id is 1 - 365, date is in mm/dd format for simplicity
       in this CRM"""

    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    date = DB.Column(DB.String(20), nullable=False)
    name = DB.Column(DB.String(15), nullable=False)

    def __repr__(self):
        return "<Day: {}>".format(self.name)

class Client(DB.Model):
    
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    name = DB.Column(DB.String(30), nullable=False)
    age = DB.Column(DB.BigInteger, nullable=False)

class Appointment(DB.Model):
    id = DB.Column(DB.String(25), primary_key=True, nullable=False) 
    day_id = DB.Column(DB.BigInteger, DB.ForeignKey('day.id'))
    day = DB.relationship('Day', backref=DB.backref('appointments'),
                          lazy=True)
    time = DB.Column(DB.BigInteger, nullable=False)
    # appointment will need an existing client's id
    client_id = DB.Column(DB.BigInteger, DB.ForeignKey('client.id'))
    client = DB.relationship('Client', backref=DB.backref('appointments'),
                                                          lazy=True)
    def __repr__(self):
        return self.time
