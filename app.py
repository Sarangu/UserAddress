import flask
from flask import Flask, Response, request, render_template, redirect
from flask_cors import CORS
import json
import logging
from datetime import datetime
import subprocess
import os

import utils.rest_utils as rest_utils
import google.oauth2.credentials
import google_auth_oauthlib.flow

from application_services.UsersResource.user_service import UserResource
from database_services.RDBService import RDBService as RDBService

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)

##################################################################################################################
# Oauth Credentials
with open('secret_key.txt') as f:
    SECRET_KEY = f.readline()
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v2'
app.secret_key = SECRET_KEY
##################################################################################################################

# DFF TODO A real service would have more robust health check methods.
# This path simply echoes to check that the app is working.
# The path is /health and the only method is GETs
@app.route("/health", methods=["GET"])
def health_check():
    rsp_data = {"status": "healthy", "time": str(datetime.now())}
    rsp_str = json.dumps(rsp_data)
    rsp = Response(rsp_str, status=200, content_type="app/json")
    return rsp

@app.route('/')
def index():
  return print_index_table()

@app.route('/users', methods=['GET', 'POST'])
def user_collection():
    if flask.request.method == 'GET':
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        field_list = request.args.get('field')
        last_name = request.args.get('last_name')
        template = None
        if last_name is not None:
            template = {"last_name":last_name}
        res = UserResource.get_by_template(template, limit, offset, field_list)
        if len(res)!= 0:
            status = 200
        else:
            status = 404
        rsp = Response(json.dumps(res, default=str), status=status, content_type="application/json")
        return rsp
    else:
        template = request.get_json()
        res = UserResource.add_template_to_table(template)
        if res != 0:
            resp = "Record(s) successfully inserted!"
        else:
            resp = "Could not insert, please check input and try again!"
        rsp = Response(json.dumps(resp, default=str), status=201, content_type="application/json")
        return rsp


@app.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def specific_user(user_id):
    if flask.request.method == 'GET':
        res = UserResource.get_by_primary_key(user_id)
        if len(res)!= 0:
            status = 200
        else:
            status = 404
        rsp = Response(json.dumps(res, default=str), status=status, content_type="application/json")
        return rsp
    elif flask.request.method == "DELETE":
        res = UserResource.delete_by_primary_key(user_id)
        if res != 0:
            resp = "Record(s) successfully deleted!"
        else:
            resp = "Could not delete, does not exist!"
        rsp = Response(json.dumps(resp, default=str), status=204, content_type="application/json")
        return rsp
    else:
        template = request.get_json()
        res = UserResource.update_by_primary_key(user_id, template)
        if res == 1:
            resp = "Record(s) successfully updated!"
        elif res == 0:
            resp = "Could not update, does not exist!"
        elif res == 2:
            resp = "Invalid/Bad data, try again!"
        rsp = Response(json.dumps(resp, default=str), status=200, content_type="application/json")
        return rsp


@app.route('/users/<user_id>/address', methods=['GET', 'PUT', 'DELETE', 'POST'])
def user_address(user_id):
    if flask.request.method == 'GET':
        res = UserResource.get_address_by_user_no(user_id)
        if len(res)!= 0:
            status = 200
        else:
            status = 404
        rsp = Response(json.dumps(res, default=str), status=status, content_type="application/json")
        return rsp
    elif flask.request.method == "DELETE":
        res = UserResource.delete_address_by_user_no(user_id)
        if res != 0:
            resp = "Record(s) successfully deleted!"
        else:
            resp = "Could not delete, does not exist!"
        rsp = Response(json.dumps(resp, default=str), status=204, content_type="application/json")
        return rsp
    elif flask.request.method == 'PUT':
        template = request.get_json()
        res = UserResource.update_address_by_user_no(user_id, template)
        if res != 0:
            resp = "Record(s) successfully updated!"
        else:
            resp = "Could not update, does not exist!"
        rsp = Response(json.dumps(resp, default=str), status=200, content_type="application/json")
        return rsp

    else:
        check = UserResource.get_by_primary_key(user_id)
        if check:
            template = request.get_json()
            res = UserResource.add_address_for_user(user_id, template)
            if res != 0:
                resp = "Record(s) successfully inserted!"
            else:
                resp = "Could not insert, please check input and try again!"
            rsp = Response(json.dumps(resp, default=str), status=201, content_type="application/json")
            return rsp
        else:
            resp = "User does not exist!"
            rsp = Response(json.dumps(resp, default=str), status=200, content_type="application/json")
            return rsp


# @app.route('/<db_schema>/<table_name>/<column_name>/<prefix>')
# def get_by_prefix(db_schema, table_name, column_name, prefix):
#     res = RDBService.get_by_prefix(db_schema, table_name, column_name, prefix)
#     rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
#     return rsp

########## Oauth Authorization ###################################################################################################

@app.route('/login')
def test_api_request():
  return render_template('index.html')

## TODO
## duplicate email
@app.route('/submit', methods = ['POST'])
def signup():
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    pnumber = request.form['pnumber']
    street_number = request.form['street_number']
    street_name1 = request.form['street_name1']
    city = request.form['city']
    state = request.form['state']
    postal_code = request.form['postal_code']

    new_user = {
        "last_name": lname,
        "first_name": fname,
        "email": email,
        "phone_number": pnumber
    }
    address_details = {
        "street_number": street_number,
        "street_name1" : street_name1,
        "city" : city,
        "state" : state,
        "postal_code": postal_code
    }
    res = UserResource.add_template_to_table(new_user)
    if res != 0:
        resp = "Record(s) successfully inserted!"
    else:
        resp = "Could not insert, please check input and try again!"
    rsp = Response(json.dumps(resp, default=str), status=201, content_type="application/json")

    # Insert address details
    res = UserResource.get_by_template(new_user, None, None, None)
    user_no = res[0]['user_no']
    res = UserResource.add_address_for_user(user_no, address_details)
    if res != 0:
        resp = "Address(s) successfully updated!"
    else:
        resp = "Could not insert, please check input and try again!"
    rsp = Response(json.dumps(resp, default=str), status=201, content_type="application/json")
    print('Address successfully updated')
    return redirect('/users')

@app.route('/authorize')
def authorize():
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
  print(flow.redirect_uri)
  authorization_url, state = flow.authorization_url(
      access_type='offline')
  flask.session['state'] = state
  return flask.redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
  state = flask.session['state']

  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
  authorization_response = flask.request.url
  flow.fetch_token(authorization_response=authorization_response)
  credentials = flow.credentials
  flask.session['credentials'] = credentials_to_dict(credentials)
  return flask.redirect(flask.url_for('test_api_request'))

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

def print_index_table():
  return ('<table>' +
          '<tr><td><a href="/authorize"> Login to your account </a></td>' +
          '<tr><td><a href="/login"> Continue as Guest </a></td>' +
          '</td></tr></table>')

if __name__ == '__main__':
    # subprocess.call(('python3 static.py'), shell=True)
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run('localhost', 5000, debug=True)
