import os


class Config(object):
    SECRET_KEY = os.environ['GRILLMEISTER_SECRET']
    BESTELLUNGEN_FILE = 'bestellungen.json'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    