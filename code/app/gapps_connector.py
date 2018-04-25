# -*- coding: utf-8 -*-
import logging

# Google
import httplib2
from apiclient import discovery
from oauth2client.file import Storage
from oauth2client import client
# from oauth2client import tools

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import flask
from flask import request, session

import os

from app import app

#Variables
google_access_file = app.config['GOOGLE_API_ACCESS']

def get_credential_file(google_access_file, scope):
    credential_dir = os.path.dirname(google_access_file) + '/.credentials'
    credential_file = credential_dir + '/' + scope.split('/')[-1] + '.json'
    return(credential_file)

def get_credentials(google_access_file,scope):
    credential_file = get_credential_file(google_access_file,scope)
    store = Storage(credential_file)
    credentials = store.get()
    #found_scope = False
    #for allowed_scope in credentials.scopes:
    #    if scope == allowed_scope:
    #        found_scope = True
    #if not credentials or credentials.invalid or not found_scope:
    if not credentials or credentials.invalid:
        #logging.info('Credentials not found')
        return False
    else:
        #logging.info('Credentials fetched successfully')
        return credentials

@app.route('/oauth2callback')
def oauth2callback():

    try:
        gapi_scope=request.args['gapi_scope']
        #google_access_file=request.args['google_access_file']
        session['gapi_scope'] = gapi_scope
        #session['google_access_file'] = google_access_file
    except:
        gapi_scope=session['gapi_scope']
        #google_access_file=session['google_access_file']

    google_service = gapi_scope.split('/')[-1]
    app.logger.info("Google Service {}".format(google_service))
    referral_uri = flask.request.referrer or '/'
    app.logger.info("Refferal url {}".format(referral_uri))
    redirect_uri = flask.request.base_url
    app.logger.info("Redirect url {}".format(redirect_uri))

    flow = client.flow_from_clientsecrets(
        google_access_file,
        scope=gapi_scope,
        redirect_uri = redirect_uri)
    flow.params['include_granted_scopes'] = 'true'
    flow.params['access_type'] = 'offline'
    flow.params['approval_prompt'] = 'force'

    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        app.logger.info("Redirecting to auth_uri {}".format(auth_uri))
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        credential_file = get_credential_file(google_access_file,gapi_scope)
        open(credential_file,'w+').write(credentials.to_json())
        credentials_in_session = 'credentials_' + google_service
        flask.session[credentials_in_session] = credentials.to_json()
        app.logger.info("User authenticated, redirecting to referral_uri {}".format(referral_uri))
        return flask.redirect(referral_uri)

def DriveInizialize(drive_access_scope,google_access_file):
    credential_file = get_credential_file(google_access_file, drive_access_scope)
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(credentials_file=credential_file)

    if gauth.credentials is None:
        app.logger.info("Redirecting to oauth2callback, gauth.credentials is none")
        return flask.redirect(flask.url_for('oauth2callback',gapi_scope=drive_access_scope,google_access_file=google_access_file))
    elif gauth.access_token_expired:
        app.logger.info("Access token is expired, refreshing")
        gauth.Refresh()
    else:
        app.logger.info("gauth Authorizing")
        gauth.Authorize()

    drive = GoogleDrive(gauth)
    return(drive)


def CalendarInizialize(cal_access_scope,google_access_file):
    credentials = get_credentials(google_access_file,cal_access_scope)
    if credentials:
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        return(service)
    else:
        return(False)
