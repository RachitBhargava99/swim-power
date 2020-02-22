from flask import Blueprint, request
from backend.models import User
from backend import db, bcrypt
import json
from backend.users.utils import send_reset_email

users = Blueprint('users', __name__)


# End-point to enable a user to log in to the website
@users.route('/login', methods=['GET', 'POST'])
def login():
    request_json = request.get_json()
    if request_json.get('isSnap'):
        display_name = request_json['display_name']
        snap_pic = request_json['snap_pic']
        user = User.query.filter_by(name=display_name, snapPic=snap_pic).first()
        if user:
            final_dict = {
                'id': user.id,
                'auth_token': user.get_auth_token(),
                'name': user.name,
                'email': user.email,
                'status': 0
            }
            return json.dumps(final_dict)
        else:
            return json.dumps({'status': 1, 'error': "You need to register before you can log in."})
    email = request_json['email']
    password = request_json['password']
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        final_dict = {
            'id': user.id,
            'auth_token': user.get_auth_token(),
            'name': user.name,
            'email': user.email,
            'status': 0
        }
        return json.dumps(final_dict)
    else:
        final_dict = {
            'status': 1,
            'error': "The provided combination of email and password is incorrect."
        }
        return json.dumps(final_dict)


# End-point to enable a user to register on the website
@users.route('/register', methods=['POST'])
def normal_register():
    request_json = request.get_json()
    print(request_json)
    if request_json.get('isSnap'):
        user = User(email="snapchat@snapchat.com", password="password", name=request_json['name'], isSnap=True,
                    snapPic=request_json['snapPic'])
        db.session.add(user)
        db.session.commit()
        return json.dumps({'id': user.id, 'status': 0})
    if User.query.filter_by(email=request_json['email']).first():
        return json.dumps({'status': 1, 'output': User.query.filter_by(email=request_json['email']).first().email,
                          'error': "User Already Exists"})
    email = request_json['email']
    hashed_pwd = bcrypt.generate_password_hash(request_json['password']).decode('utf-8')
    name = request_json['name']
    # noinspection PyArgumentList
    user = User(email=email, password=hashed_pwd, name=name)
    db.session.add(user)
    db.session.commit()
    return json.dumps({'id': user.id, 'status': 0})


# End-point to enable a user to change their access level to administrator
@users.route('/admin/add', methods=['GET', 'POST'])
def master_add():
    request_json = request.get_json()
    user = User.query.filter_by(email=request_json['email']).first()
    user.isAdmin = True
    db.session.commit()
    return json.dumps({'status': 0})


# End-point to enable a user to request a new password
@users.route('/password/request_reset', methods=['GET', 'POST'])
def request_reset_password():
    request_json = request.get_json()
    user = User.query.filter_by(email=request_json['email']).first()
    if user:
        send_reset_email(user)
        return json.dumps({'status': 0})
    else:
        return json.dumps({'status': 1, 'error': "User Not Found"})


# End-point to enable a user to verify their password reset request
@users.route('/backend/password/verify_token', methods=['GET', 'POST'])
def verify_reset_token():
    request_json = request.get_json()
    user = User.verify_reset_token(request_json['token'])
    if user is None:
        return json.dumps({'status': 1, 'error': "Sorry, the link is invalid or has expired. Please submit password reset request again."})
    else:
        return json.dumps({'status': 0})


# End-point to enable a user to set up a new password
@users.route('/backend/password/reset', methods=['GET', 'POST'])
def reset_password():
    request_json = request.get_json()
    user = User.verify_reset_token(request_json['token'])
    if user is None:
        return json.dumps({'status': 1,
                           'error': "Sorry, the link is invalid or has expired. Please submit password reset request again."})
    else:
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pwd
        db.session.commit()
        return json.dumps({'status': 0})


# Checker to see if the server is up and running
@users.route('/test', methods=['GET'])
def test():
    return "Hello World"