#encoding=utf-8
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from forms import WurstOrderForm, DeleteOrderForm, IndexForm
from models import Bestellungen
import config

import os

#TODO: Nachträgliche Änderungen der getätigten Bestellungen

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

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


def initEmptyDatabases():
    db.create_all()

@app.route('/', methods=['GET', "POST"])
def index():
    form=IndexForm(request.form)
    if request.method == "POST":
        if not os.path.exists(config.EVENTS_FILE):
            initEmptyDatabases()
        #create event
        #create new Database or une database
        new_event = DB_Events(name=form.name.data, date=form.date.data, offer=form.offer.data)
        db.session.add(new_event)
        db.session.commit()
        
        #TODO: Datenbank umbenennen, config anpassen, Datenbank testen
        
        return render_template('index.html', created=True, form=form)
    return render_template('index.html', form=form)

@app.route('/grillen', methods=['GET', 'POST'])
def wurstOrder():
    form=WurstOrderForm(request.form)
    print('Valid input: ' + str(form.validate()))
    if request.method == 'POST':
        if not os.path.exists(config.BESTELLUNGEN_FILE):
            initEmptyDatabases()
        new_order = DB_Bestellungen(name=form.name.data, bratwurst=form.bratwurst.data, schinkengriller=form.schinkengriller.data, broetchen=form.broetchen.data*(int(form.bratwurst.data)+int(form.schinkengriller.data)), selbstversorger=form.selbstversorger.data)
        db.session.add(new_order)
        db.session.commit()
        return render_template('order.html', bestellt=True, form=form)
    return render_template('order.html', form=form)

    #TODO: Fehler bei ungültiger Eingabe (alles 0; brötchen ohne was anderes)

@app.route('/summary', methods=['GET'])
def summary():
    if os.path.exists(config.BESTELLUNGEN_FILE):
        #namen = db.session.execute("SELECT name FROM bestellungen")
        #bestellungen = db.session.execute("SELECT bratwurst FROM bestellungen")
        #output = ""
        db_req = db.session.execute("SELECT * FROM bestellungen")
        keys = db_req.keys()
        entries = db_req.fetchall()
        print(keys)
        print(entries)
        #for x in namen.fetchall():
        #    name += "%s" % (x)
        #for y in bestellungen.fetchall():
        #    bestellung += "%s" % (y)
        #        output +=  "<strong>%s</strong>: %s " % (request.keys()[y], x[y])
        #    output += "<br>"
        #output += "<br>Teilnehmeranzahl: %s<br><br>" % x[0]
        
        #for key in request.keys()[2:]:
        #    output += "%s: %s<br>" % (key, db.session.execute("SELECT SUM(%s) FROM bestellungen" % key).fetchall()[0][0]) #execute funktionert; sum rechnet alle zuammen, [0][0] "entfernt" die liest und tuple
         
        #TODO: Richtiger Brötchenzähler
        #TODO: Schöner machen
        return render_template('summary.html', keys=keys, entries=entries)
    
    elif not os.path.exists(config.BESTELLUNGEN_FILE):
        return "No orders!"
    #return str(output)
    

@app.route('/delete', methods=['GET', 'POST'])
def deleteOrderForm():
    form=DeleteOrderForm(request.form)
    if request.method == 'POST':
        print(form.delete_secret.data)
        print(form.confirm_delete.data)
        if form.delete_secret.data == "Mettwoch" and form.confirm_delete.data:
            return deleteOrders()
        return "Hau ab!"
    return render_template('delete_order.html', form=form)

def deleteOrders():
    if os.path.exists(config.BESTELLUNGEN_FILE):
        os.remove(config.BESTELLUNGEN_FILE)
        return("Bestellungen erfolgreich gelöscht.")
    return("Keine Bestellungen zum Löschen.")

