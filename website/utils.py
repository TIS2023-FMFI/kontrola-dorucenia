from flask_mail import Mail, Message
from .models import *
from . import *
from .config import get_env
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
    key = get_env("SECRET_KEY")
    app.config['SECRET_KEY'] = key.encode()
    app.config['SQLALCHEMY_DATABASE_URI'] = get_env("SQLALCHEMY")
    app.config['MAIL_SERVER'] = get_env("MAIL_SERVER")
    app.config['MAIL_PORT'] = int(get_env("MAIL_PORT"))
    app.config['MAIL_USE_TLS'] = bool(int(get_env("MAIL_USE_TLS")))
    app.config['MAIL_USE_SSL'] = bool(int(get_env("MAIL_USE_SSL")))
    app.config['MAIL_USERNAME'] = get_env("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = get_env("MAIL_PASSWORD")
    with app.app_context():
        msg = Message(subject, sender=get_env("MAIL_USERNAME"), recipients=[email])
        msg.body = body
        return Mail(app).send(msg)
