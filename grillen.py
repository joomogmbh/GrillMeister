from flask import Flask, render_template, request

from forms import WurstOrderForm, DeleteOrderForm
from models import Bestellungen
import config

# TODO switch to a light DB, instead of json
import json
import os



app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

def initEmptyOrderFile():
    with open(config.BESTELLUNGEN_FILE, 'w') as f:
        data = json.dumps({})
        f.write(data)

@app.route('/', methods=['GET'])
def index():
    return "Try /grillen, or /summary"

@app.route('/grillen', methods=['GET', 'POST'])
def wurstOrder():
    form=WurstOrderForm(request.form)
    print('Valid input: ' + str(form.validate()))
    if request.method == 'POST':
        kunstdarm = {'bratwurst': form.bratwurst.data, 'schinkengriller': form.schinkengriller.data, 'selbstversorger': form.selbstversorger.data}
        bestellung = Bestellungen(form.name.data, kunstdarm)
        # If there is currently not order JSON, initialize it
        if not os.path.exists(config.BESTELLUNGEN_FILE):
            initEmptyOrderFile()
        with open(config.BESTELLUNGEN_FILE, 'r') as f:
            data = json.load(f)
            #f.seek(0)
        with open(config.BESTELLUNGEN_FILE, 'w') as f:
            data[bestellung.getName()] = bestellung.getBestellungen()
            #data['bestellungen'].append(bestellung.getBestellungDict())
            f.write(json.dumps(data))
#        with open ('output.txt', 'a') as f:
#            f.write(str(bestellung))
        return render_template('index.html', bestellt=True, form=form)
    return render_template('index.html', form=form)

@app.route('/summary', methods=['GET'])
def summary():
    if os.path.exists(config.BESTELLUNGEN_FILE):
        with open(config.BESTELLUNGEN_FILE, 'r') as f:
            data = json.load(f) 
        output = "Teilnehmer: %s<br><br>" % len(data)
        for participant in sorted(data):
            output += "<strong>%s:</strong> " % participant
            for order in sorted(data[participant]):
                output += "%s: %s, " % (order, data[participant][order])
            output = output[:-2] + "<br>"
        output += "<br>"
        order_possibilities = data[participant]
        for order in sorted(order_possibilities):
            output += "%s: %s<br>" % (order, sum([int(data[x][order]) for x in data]))
    elif not os.path.exists(config.BESTELLUNGEN_FILE):
        initEmptyOrderFile()
        output = "No orders!"
    return str(output)

# TODO urgently needs to be reworked, this is just a temp way to reset
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

