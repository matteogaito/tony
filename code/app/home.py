# -*- coding: utf-8 -*-

import flask
import werkzeug
import httplib2

import flask_gapps_connector

from apiclient import discovery
from flask import render_template

from app import app

def getDriveTree():
    """ Show Google Drive Tree
    """
    drive_scope = 'https://www.googleapis.com/auth/drive'
    google_access_file = app.config['GOOGLE_API_ACCESS']
    credentials = flask_gapps_connector.get_credentials(google_access_file=google_access_file, scope=drive_scope)

    print(credentials)

    if credentials:
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('drive', 'v3', http=http)
        query = "'root' in parents and mimeType = 'application/vnd.google-apps.folder'"
        sort = "modifiedTime desc"
        results = service.files().list(
            q=query,orderBy=sort,pageSize=20,fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        return items
    else:
        return flask.redirect(flask.url_for('oauth2callback',gapi_scope=drive_scope,google_access_file=google_access_file))

@app.route("/")
def home():
  mydrivedirs = getDriveTree()
  #Do redirect if the response of the function is a redirect
  if isinstance(mydrivedirs, werkzeug.wrappers.Response):
    return(mydrivedirs)
  #return render_template('home.html', mydrivedirs=mydrivedirs, mytenevents=mytenevents)
  return render_template('home.html', mydrivedirs=mydrivedirs)
  return("ok")
