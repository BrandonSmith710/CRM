from flask import Flask
from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()

class Client(DB.Model):

    # client will have list of appointments through backref

    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)

    name = DB.Column(DB.String(30), nullable=False)

    age = DB.Column(DB.BigInteger, nullable=False)




class Day(DB.Model):
    # id is 1 - 365
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    
    # date is string mm/dd
    date = DB.Column(DB.String(20), nullable=False)

    # or use Appointment.Day ( i believe)
    name = DB.Column(DB.String(15), nullable=False)

    # def __contains__(self, n):

    #     return n in self.date


    # each day also has a list of appointment objects
    # accessed by Day.Appointments

    def __repr__(self):

        return "<Day: {}>".format(self.name)

class Appointment(DB.Model):
    id = DB.Column(DB.String(25), primary_key=True, nullable=False) 

    day_id = DB.Column(DB.BigInteger, DB.ForeignKey('day.id'))      # add list of appointments to each day

    day = DB.relationship('Day', backref=DB.backref('appointments'), lazy=True)

    time = DB.Column(DB.BigInteger, nullable=False)

    # appointment will need an existing client's id in order to be instantiated

    client_id = DB.Column(DB.BigInteger, DB.ForeignKey('client.id'))

    client = DB.relationship('Client', backref=DB.backref('appointments'), lazy=True)

    def __repr__(self):
        return self.time


# class Client(DB.Model):

#     # id = 

#     name = DB.relationship('Appointment', backref=DB.backref('clients'), lazy=True)
#                      # provides lists apppointment.client(s)
#                      # and client.appointment
                     

#     # balance = 

#     # history = 