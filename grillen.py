#encoding=utf-8
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from forms import WurstOrderForm, DeleteOrderForm
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
    broetchen = db.Column(db.Boolean, default=True)
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

def initEmptyOrderFile():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    return "Try /grillen, or /summary"

@app.route('/grillen', methods=['GET', 'POST'])
def wurstOrder():
    form=WurstOrderForm(request.form)
    print('Valid input: ' + str(form.validate()))
    if request.method == 'POST':
        if not os.path.exists(config.BESTELLUNGEN_FILE):
            initEmptyOrderFile()
        new_order = DB_Bestellungen(name=form.name.data, bratwurst=form.bratwurst.data, schinkengriller=form.schinkengriller.data, broetchen=form.broetchen.data, selbstversorger=form.selbstversorger.data)
        db.session.add(new_order)
        db.session.commit()
        return render_template('index.html', bestellt=True, form=form)
    return render_template('index.html', form=form)

@app.route('/summary', methods=['GET'])
def summary():
    if os.path.exists(config.BESTELLUNGEN_FILE):
        #data = eval(DB_Bestellungen.query.all())
        #output = "Teilnehmer: %s<br><br>" % len(DB_Bestellungen.query.all())
        #for participant in DB_Bestellungen.query.all():
         ##   participant = eval(str(participant))
         #   for key, value in participant.items():
         #       output += "<strong>%s</strong>: %s" % (key, value)
        #    output += "<br>"
        #output += "<br>"
        #for key, value in participant.items():
         #   output += "Value: %s" % ([key for key in value.values[key]])
       # print(output)
        print(db.select([DB_Bestellungen]).where(DB_Bestellungen.column.bratwurst == 0))
                                
                
    elif not os.path.exists(config.BESTELLUNGEN_FILE):
        #initEmptyOrderFile()
        output = "No orders!"
    return str(output)

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

