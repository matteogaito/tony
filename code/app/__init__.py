import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

#from app import route,telegram_connector,home
from app import home
from app import sprea_downloader
from app import packt_notifier
from app import job_documentation
