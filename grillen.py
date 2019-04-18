from flask import Flask, render_template, request

from forms import WurstOrderForm
from models import Bestellungen
import config

# TODO switch to a light DB, instead of json
import json
import os



app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

def initEmptyOrderFile():
    with open(config.BESTELLUNGEN_FILE, 'w') as f:
        data = json.dumps({'bestellungen' : []})
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
        with open(config.BESTELLUNGEN_FILE, 'r+') as f:
            read_data = f.read()
            data = json.loads(read_data)
            f.seek(0)
            data['bestellungen'].append(bestellung.getBestellungDict())
            f.write(json.dumps(data))
#        with open ('output.txt', 'a') as f:
#            f.write(str(bestellung))
    return render_template('index.html', title='WURSTBESTELLUNG', form=form)

@app.route('/summary', methods=['GET'])
def summary():
    if os.path.exists(config.BESTELLUNGEN_FILE):
        with open(config.BESTELLUNGEN_FILE, 'r') as f:
            read_data = f.read()
            data = json.loads(read_data)
    else:
        initEmptyOrderFile()
    return str(data)

# TODO urgently needs to be reworked, this is just a temp way to reset
@app.route('/delete', methods=['GET'])
def deleteOrders():
    if os.path.exists(config.BESTELLUNGEN_FILE):
        os.remove(config.BESTELLUNGEN_FILE)
        return("Bestellungen erfolgreich gelöscht.")
    return("Keine Bestellungen zum Löschen.")

