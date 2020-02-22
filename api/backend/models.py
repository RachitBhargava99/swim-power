from backend import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from flask import current_app
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(127), nullable=False)
    email = db.Column(db.String(63), unique=False, nullable=False)
    password = db.Column(db.String(63), unique=False, nullable=False)
    isSnap = db.Column(db.Boolean, nullable=False, default=False)
    snapPic = db.Column(db.String(255), nullable=True)
    isCoach = db.Column(db.Boolean, nullable=False, default=False)

    def get_auth_token(self, expires_seconds=86400):
        s = Serializer(current_app.config['SECRET_KEY'], expires_seconds)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def get_reset_token(self, expires_seconds=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_seconds)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User ID {self.id}"


class TowerRecord(db.Model):
    """
    A database model class to store data received from power tower

    ...

    Attributes
    ----------
    id : int
        ID of the student
    swimmer_id : int
        Swimmer ID, as stored in User table
    distance : float
        Distance, as given by power tower, used by the swimmer
    timestamp : datetime.datetime
        Timestamp of when the entry was received
    """
    id = db.Column(db.Integer, primary_key=True)
    swimmer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    distance = db.Column(db.Float, nullable=False, default=0.0)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, swimmer_id, distance, timestamp=datetime.now()):
        """
        Parameters
        ----------
        swimmer_id : int
            Swimmer ID, as stored in User table
        distance : float
            Distance, as given by power tower, used by the swimmer
        timestamp : datetime.datetime
            Timestamp of when the entry was received
        """
        self.swimmer_id = swimmer_id
        self.distance = distance
        self.timestamp = timestamp
