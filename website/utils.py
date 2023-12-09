from flask_mail import Mail, Message
from .models import User
from . import *
from flask import current_app

# Find user by id or email
def find_user(id: int = None, email: str = None):
    users_from_db = User.query.all()
    for user in users_from_db:
        if (id and user.id == id) or (email and user.email == email):
            return user
    return False

def send_email(subject: str, body: str):
    msg = Message(subject, sender='t402829@gmail.com', recipients=["t402829@gmail.com"])
    msg.body = body
    return Mail(current_app).send(msg)