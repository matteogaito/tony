# -*- coding: utf-8 -*-

import flask
from flask-gapps-connector import *

def getDriveTree():
    """ Show Google Drive Tree
    """
    drive_scope = 'https://www.googleapis.com/auth/drive'
    credentials = gapi_connector.get_credentials(scope=drive_scope)

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
        return flask.redirect(flask.url_for('oauth2callback',gapi_scope=drive_scope))

@app.route("/")
def home():
  mydrivedirs = getDriveTree()
  if isinstance(mydrivedirs, werkzeug.wrappers.Response):
      return mydrivedirs
