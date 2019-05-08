import os



SECRET_KEY = os.environ['GRILLMEISTER_SECRET']
BESTELLUNGEN_FILE = 'bestellungen.db'
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

