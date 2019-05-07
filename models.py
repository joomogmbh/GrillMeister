from grillen import db
from sqlalchemy import Column, Integer, String



class DB_Bestellungen(db.Model):
    __tablename__ = 'bestellungen'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    bratwurst = db.Column(db.Integer)
    schinkengriller = db.Column(db.Integer)
    broetchen = db.Column(db.Boolean, default=True)
    
    def __init__(self, name, bratwurst, schinkengriller, broetchen):
        self.name = name
        self.bratwurst = bratwurst
        self.schinkengriller = schinkengriller
        self.broetchen = broetchen
        
    def __repr__(self):
        return '<DB_Bestellungen %r>' % (self.name)

class Bestellungen():
    def __init__(self, name, bestellungen):
        self.name = name
        self.bestellungen = bestellungen
        
    def getBestellungDict(self):
        return {self.name : self.bestellungen}
        
    def getName(self):
        return self.name
        
    def getBestellungen(self):
        return self.bestellungen      
  
    def __str__(self):
        return str(self.name) + str(self.bestellungen)
