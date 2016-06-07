#! /usr/bin/python3
import notatnik
import create_table
from flask import Flask, g, request
from settings import bot

HOST = '87.246.193.79'
# FQDN or ip address of the server (should be same as used when generating
# SSL certificate)
PORT = 8443
CERT = 'ssl/webhook_cert.crt'
CERT_KEY = 'ssl/webhook_cert.key

app = Flask(__name__)
app.config['SERVER_NAME'] = 'arch-laptop'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = create_table.create_table()
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_databse', None)
    if db is not None:
        db.close_connection()
