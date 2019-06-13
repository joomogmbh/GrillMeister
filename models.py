import grillen
from flask_sqlalchemy import SQLAlchemy



print(dir(grillen))
db = SQLAlchemy(grillen.app)
        
class DB_Bestellungen(db.Model):
    __tablename__ = 'bestellungen'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    bratwurst = db.Column(db.Integer)
    schinkengriller = db.Column(db.Integer)
    broetchen = db.Column(db.Integer, default=True)
    selbstversorger = db.Column(db.Boolean, default=False)
    
    def __init__(self, name, bratwurst, schinkengriller, broetchen, selbstversorger):
        self.name = name
        self.bratwurst = bratwurst
        self.schinkengriller = schinkengriller
        self.broetchen = broetchen
        self.selbstversorger = selbstversorger
        
    def __repr__(self):
        #return 'Name: %s Bratwurst: %s Schinkengriller: %s Broetchen: %s Selbstversorger: %s' % (self.name, self.bratwurst, self.schinkengriller, self.broetchen, self.selbstversorger)
        return str({self.name: {"Bratwurst":self.bratwurst,"Schinkengriller":self.schinkengriller,"Brötchen":self.broetchen,"Selbstversorger":self.selbstversorger}})
        
class DB_Events(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    date = db.Column(db.Date, unique=True)
    offer = db.Column(db.String)
    
    def __init__(self, name, date, offer):
        self.name = name
        self.date = date
        self.offer = offer
        
    def __repr__(self):
        return "Events"
