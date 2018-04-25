# -*- coding: utf-8 -*-

from app import app

import os

import google.oauth2.credentials
import google_auth_oauthlib.flow
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import flask
from flask import request, session, jsonify

google_access_file = app.config['GOOGLE_API_ACCESS']
credential_dir = os.path.dirname(google_access_file) + '/.credentials'

def get_credential_file(google_access_file, scope):
    credential_dir = os.path.dirname(google_access_file) + '/.credentials'
    credential_file = credential_dir + '/' + scope.split('/')[-1] + '.json'
    return(credential_file)

@app.route('/authorize')
def authorize():
    try:
        gapi_scope = request.args['gapi_scope']
        session['gapi_scope'] = gapi_scope
    except:
        gapi_scope=session['gapi_scope']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file( google_access_file, gapi_scope )
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
      # This parameter enables offline access which gives your application
      # both an access and refresh token.
      access_type = 'offline',
      # This parameter enables incremental auth.
      include_granted_scopes = 'true',
      approval_prompt = 'force' )

    # Store the state in the session so that the callback can verify that
    # the authorization server response.
    flask.session['state'] = state

    return flask.redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verify the authorization server response.
    state = flask.session['state']

    try:
        gapi_scope = request.args['gapi_scope']
        session['gapi_scope'] = gapi_scope
    except:
        gapi_scope = session['gapi_scope']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        google_access_file, scopes=gapi_scope, state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credential to file
    credentials = flow.credentials
    print(dir(credentials))
    print(type(credentials))
    credential_file = get_credential_file(google_access_file, gapi_scope)
    print(credential_file)
    open(credential_file, 'w+').write(jsonify(credentials))
    return flask.redirect(flask.url_for('index'))


def DriveInizialize(drive_access_scope, google_access_file):
    credential_file = get_credential_file(google_access_file, drive_access_scope)
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(credentials_file=credential_file)

    if gauth.credentials is None:
        return flask.redirect(flask.url_for('authorize', gapi_scope=drive_access_scope))
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    drive = GoogleDrive(gauth)
    return(drive)
