import flask
from flask import Flask, Response, request, render_template
from flask_cors import CORS
import json
import logging
from datetime import datetime
import subprocess

import utils.rest_utils as rest_utils

from application_services.UsersResource.user_service import UserResource
from database_services.RDBService import RDBService as RDBService

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)


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
def hello_world():
    return render_template('index.html')


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


if __name__ == '__main__':
    subprocess.call(('python3 static.py'), shell=True)
    app.run(host="0.0.0.0", port=5000)
