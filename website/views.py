from flask import Blueprint, render_template, request, flash, jsonify, current_app
from flask_login import login_required, current_user
from flask_mail import Mail, Message
from . import db
import json
import pandas as pd

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    i = 0
    return render_template("order_search.html", user=current_user)


@views.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    return render_template("user_info.html", user=current_user)


@views.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    # tu treba nacitat objednavky, zistit ci objednavka existuje, vypisat o nej informacie, do htmlka spravit button na poslanie requestu
    # workbook = pd.read_excel('../example.xls')
    # rows = "Column First Name in excel document example.xls contains values : <br>"
    # for index, row in workbook.iterrows():
    #     rows += row['First Name'] + ' <br> '
    return render_template("order.html", user=current_user)


@views.route('/send-request', methods=['GET', 'POST'])
@login_required
def request():
    subject = 'Hello from your Flask app!'
    body = 'This is a test email sent from a Flask app.'

    msg = Message(subject, sender='t402829@gmail.com', recipients=["mattuss12@gmail.com"])
    msg.body = body

    try:
        Mail(current_app).send(msg)
        return 'Email sent successfully!'
    except Exception as e:
        return 'Error sending email: ' + str(e)
