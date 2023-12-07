from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Request')
    def changePassword(self,new_password):
        self.password = new_password


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_code = db.Column(db.String(11))
    carrier_email = db.Column(db.String)
    send_date = db.Column(db.Date)
    send_time = db.Column(db.Time)
    additional_message = db.Column(db.Text)
    response = db.Column(db.Boolean)
    responses = db.relationship('Response')


class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))
    type = db.Column(db.String)
    delay = db.Column(db.Boolean)
    root_cause = db.Column(db.String)
    estimated_date = db.Column(db.Date)
    estimated_time = db.Column(db.Time)
    comment = db.Column(db.Text)


class Order:
    def __init__(self, loading_ctr):
        self.loading_ctr = loading_ctr
