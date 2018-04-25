# -*- coding: utf-8 -*-
from app import app

#import sys
#sys.path.insert(0, '/vagrant/flask-gapps-connector')

from .gapps_connector import DriveInizialize, CalendarInizialize

import datetime
import logging
import flask
from flask import render_template

_log = logging.getLogger(__name__)


@app.route("/")
def index():
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    if 'credentials_drive' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback', gapi_scope=app.config['DRIVE_SCOPE']))

    _log.info('Google Drive inizialing')
    drive = DriveInizialize(app.config['DRIVE_SCOPE'], app.config['GOOGLE_API_ACCESS'])
    query = "'root' in parents and mimeType = 'application/vnd.google-apps.folder'"
    mydrivedirs = drive.ListFile({ 'q': query }).GetList()

    if 'credentials_calendar.readonly' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback', gapi_scope=app.config['CAL_SCOPE']))

    service = CalendarInizialize(app.config['CAL_SCOPE'], app.config['GOOGLE_API_ACCESS'])

    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    return render_template('home.html', mydrivedirs=mydrivedirs, myevents=events)
