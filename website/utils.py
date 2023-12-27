from flask_mail import Mail, Message
from .models import *
from . import *
from flask import current_app

# Find user by id or email
def find_user(id: int = None, email: str = None):
    users_from_db = User.query.all()
    for user in users_from_db:
        if (id and user.id == id) or (email and user.email == email):
            return user
    return False

# Find request by id
def find_request(id: int = None):
    requests_from_db = Request.query.all()
    for req in requests_from_db:
        if (id and req.id == id):
            return req
    return False

def send_email(subject: str, body: str, email: str):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = b'hs8b9e256co648'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 't402829@gmail.com'
    app.config['MAIL_PASSWORD'] = 'Pbui rzbg sabm swot '  # heslo od emailu
    with app.app_context():
        msg = Message(subject, sender='t402829@gmail.com', recipients=[email])
        msg.body = body
        return Mail(app).send(msg)
    
    
