#encoding=utf-8
from flask import Flask, render_template, request
from sqlalchemy import update
from forms import WurstOrderForm, DeleteOrderForm, IndexForm

import config

import os

#TODO: Nachträgliche Änderungen der getätigten Bestellungen

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI

# import models AFTER app is initiatlized
from models import db, DB_Bestellungen, DB_Events

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

@app.route("/events", methods=["GET"])
def events():
    if os.path.exists(config.BESTELLUNGEN_FILE):
        db_req = db.session.execute("SELECT * FROM events")
        keys = db_req.keys()
        entries = db_req.fetchall()
        print(keys)
        print(entries)
        return render_template('summary.html', keys=keys, entries=entries, title="Events")
    
    
    return "No events!"

@app.route('/grillen', methods=['GET', 'POST'])
def wurstOrder():
    form=WurstOrderForm(request.form)
    print('Valid input: ' + str(form.validate()))
    if request.method == 'POST':
        if not os.path.exists(config.BESTELLUNGEN_FILE):
            initEmptyDatabases()
        new_order = DB_Bestellungen(name=form.name.data, bratwurst=form.bratwurst.data, schinkengriller=form.schinkengriller.data, broetchen=form.broetchen.data*(int(form.bratwurst.data)+int(form.schinkengriller.data)), selbstversorger=form.selbstversorger.data)
        if DB_Bestellungen.query.filter(DB_Bestellungen.name == form.name.data).one_or_none():
            db.session.query(DB_Bestellungen).filter(DB_Bestellungen.name == form.name.data).update({DB_Bestellungen.bratwurst: form.bratwurst.data, DB_Bestellungen.broetchen: form.broetchen.data*(int(form.bratwurst.data)+int(form.schinkengriller.data)), DB_Bestellungen.schinkengriller: form.schinkengriller.data, DB_Bestellungen.selbstversorger: form.selbstversorger.data})
        else:
            db.session.add(new_order)
        db.session.commit()
        
        return render_template('order.html', bestellt=True, form=form)
    return render_template('order.html', form=form)


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
        
        totals = []
        for i, key in enumerate(keys):
            if key == 'id':
                totals.append("")
                continue
            elif key == 'name':
                totals.append("Total")
                continue
            total = 0
            for entry in entries:
                total = total + entry[i]
            totals.append(total)

        totals = tuple(totals)
        entries.append(totals)
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
        return render_template('summary.html', keys=keys, entries=entries, title="Bestellungen")
    
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

