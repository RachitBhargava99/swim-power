from flask import Blueprint, request, current_app, flash, redirect, url_for, render_template
from backend import db
from backend.models import User, TowerRecord
from backend.users.utils import token_expiration_json_response, insufficient_rights_json_response
import json

records = Blueprint('record', __name__)


# Checker to see whether or not is the server running
@records.route('/record', methods=['GET'])
def checker():
    return "Hello"


@records.route('/record/add', methods=['POST'])
def add_tower_record():
    """
    Adds a new record from swimming power tower.

    Method Type
    -----------
    POST

    JSON Parameters
    ---------------
    auth_token : str
        Authentication of the logged in user
    distance : float
        Distance from ground to be added

    Restrictions
    ------------
    User must be logged in

    JSON Returns
    ------------
    status : int
        Status code representing success status of the request
    message : str
        Message explaining the response status
    """
    request_json = request.get_json()
    auth_token = request_json['auth_token']
    user = User.verify_auth_token(auth_token)
    if user is None:
        return token_expiration_json_response
    distance = request_json['distance']
    new_record = TowerRecord(swimmer_id=user.id, distance=distance)
    db.session.add(new_record)
    db.session.commit()
    return json.dumps({'status': 0, 'message': "Entry Added Successfully"})
