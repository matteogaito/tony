# -*- coding: utf-8 -*-

#import sys
#sys.path.insert(0, '/vagrant/flask-gapps-connector')

from flask_gapps_connector import DriveInizialize

import werkzeug
from flask import render_template

from app import app

@app.route("/")
def home():
    drive = DriveInizialize( app.config['DRIVE_SCOPE'], app.config['GOOGLE_API_ACCESS'])
    #Do redirect if the response of the function is a redirect
    if isinstance(drive, werkzeug.wrappers.Response):
        return(drive)
    query = "'root' in parents and mimeType = 'application/vnd.google-apps.folder'"
    mydrivedirs = drive.ListFile({ 'q': query }).GetList()
    return render_template('home.html', mydrivedirs=mydrivedirs)
