import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

#from app import route,telegram_connector,home
from app import home