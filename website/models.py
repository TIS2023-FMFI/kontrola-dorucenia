from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Boolean)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    requests = db.relationship('Request')

    def changePassword(self, new_password):
        self.password = new_password
        session = db.session
        session.commit()

    def removeUser(self):
        session = db.session
        user_to_remove = User.query.get(self.id)
        if user_to_remove:
            session.delete(user_to_remove)
            session.commit()
            return True
        return False


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_code = db.Column(db.String(11))
    carrier_email = db.Column(db.String)
    send_date = db.Column(db.Date)
    send_time = db.Column(db.Time)
    additional_message = db.Column(db.Text)
    response = db.Column(db.Boolean)
    responses = db.relationship('Response', foreign_keys='Response.request_id')
    response_id = db.Column(db.String)

    def removeRequest(self):
        session = db.session
        try:
            session.delete(self)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error during deletion: {e}")
            return False


class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))
    response_id = db.Column(db.Integer, db.ForeignKey('request.response_id'))
    type = db.Column(db.String)
    delay_loading = db.Column(db.Boolean)
    delay_unloading = db.Column(db.Boolean)
    root_cause = db.Column(db.String)
    loading_estimated_date = db.Column(db.Date)
    loading_estimated_time = db.Column(db.Time)
    unloading_estimated_date = db.Column(db.Date)
    unloading_estimated_time = db.Column(db.Time)
    comment = db.Column(db.Text)
    loaded = db.Column(db.Boolean)
    unloaded = db.Column(db.Boolean)

    def load(self):
        self.loaded = True
        session = db.session
        session.commit()

    def unload(self):
        self.unloaded = True
        session = db.session
        session.commit()

    def set_root_cause(self, cause):
        self.root_cause = cause
        session = db.session
        session.commit()

    def set_delay_loading(self, delay):
        self.delay_loading = delay
        session = db.session
        session.commit()

    def set_delay_unloading(self, delay):
        self.delay_unloading = delay
        session = db.session
        session.commit()

    def set_loading_date(self, date):
        self.loading_estimated_date = datetime.strptime(date, '%Y-%m-%d')
        session = db.session
        session.commit()

    def set_loading_time(self, time):
        self.loading_estimated_time = datetime.strptime(time, '%H:%M').time()
        session = db.session
        session.commit()

    def set_unloading_date(self, date):
        self.unloading_estimated_date = datetime.strptime(date, '%Y-%m-%d')
        session = db.session
        session.commit()

    def set_unloading_time(self, time):
        self.unloading_estimated_time = datetime.strptime(time, '%H:%M').time()
        session = db.session
        session.commit()

    def set_comment(self, comment):
        self.comment = comment
        session = db.session
        session.commit()

    def removeResponse(self):
        session = db.session
        try:
            session.delete(self)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error during deletion: {e}")
            return False


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    string = db.Column(db.String)
    response_id = db.Column(db.String)

    def removeChat(self):
        session = db.session
        try:
            session.delete(self)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error during deletion: {e}")
            return False
