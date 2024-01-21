from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import secrets
import string
from collections import OrderedDict
from . import db
import pandas as pd

from website.models import Request, Response, User
from .excel import Evidencia_nezhod

communication = Blueprint('communication', __name__)
conversations = OrderedDict()


def generate_random_url() -> str:
    characters = string.ascii_letters + string.digits
    random_url = ''.join(secrets.choice(characters) for _ in range(20))
    existing_urls = set(conversations.keys())
    while random_url in existing_urls:  # Ak by sa nahodou vytvorila url, ktora uz existuje
        random_url = ''.join(secrets.choice(characters) for _ in range(20))
    conversations[random_url] = []
    return random_url


def getConversations() -> OrderedDict:
    return conversations


def deleteConversation(index: int) -> bool:
    if len(conversations) < index + 1:
        return False
    toDelete = conversations.items()[index]
    conversations.pop(toDelete, None)
    return True


@communication.route('/<chat_id>', methods=['GET', 'POST'])
def chat(chat_id):
    current_response = Response.query.filter(Response.response_id == chat_id).all()
    current_request = Request.query.filter(Request.response_id == chat_id).all()

    if not current_response:
        return render_template('chat.html', chat_id='err', messages="Site not found!")

    current_response = current_response[0]
    current_request = current_request[0]
    current_user = User.query.filter(current_request.user_id == User.id).first()

    if current_request.response:
        return render_template('chat.html', chat_id='err', messages="Site not found!")

    if request.method == 'POST':

        loading = request.form.get('confirm_loading')
        unloading = request.form.get('confirm_unloading')
        late_loading_value = request.form.get('late_loading')
        late_unloading_value = request.form.get('late_unloading')
        date = request.form.get('date')
        time = request.form.get('time')
        cause_delay = request.form.get('cause_delay')
        comment = request.form.get('message')
        if not comment:
            comment = "-"
        if loading:
            loaded_checkbox_value = request.form.get('loaded')
            if loaded_checkbox_value == 'loaded':
                write_response_to_excel(current_request.order_code, current_request.carrier_email,
                                        "Nákladka je vykonaná.", current_user.name, "", "")
            else:
                write_response_to_excel(current_request.order_code, current_request.carrier_email,
                                        "Nákladka sa vykoná v dohodnutom čase.", current_user.name, "", "")
        elif unloading:
            unloaded_checkbox_value = request.form.get('unloaded')
            if unloaded_checkbox_value == 'unloaded':
                write_response_to_excel(current_request.order_code, current_request.carrier_email,
                                        "Výkladka je vykonaná.", current_user.name, "", "")
            else:
                write_response_to_excel(current_request.order_code, current_request.carrier_email,
                                        "Výkladka sa vykoná v dohodnutom čase.", current_user.name, "", "")
        elif late_loading_value:
            write_response_to_excel(current_request.order_code, current_request.carrier_email,
                                    ("Vozidlo bude meškať na nákladku z dôvodu " + get_cause(cause_delay, comment) + ". " +
                                    "Predpokladaný čas nákladky: " + date + " " + time),
                                    current_user.name, comment,  get_cause(cause_delay, comment))
        elif late_unloading_value:
            write_response_to_excel(current_request.order_code, current_request.carrier_email,
                                    ("Vozidlo bude meškať na výkladku z dôvodu " + get_cause(cause_delay,
                                                                                             comment) + ". " +
                                     "Predpokladaný čas výkladky: " + date + " " + time),
                                    current_user.name, comment, get_cause(cause_delay, comment))
        current_request.response = True
        db.session.commit()
    return render_template('SK.html', chat_id=chat_id, res=current_response, req=current_request)


def write_response_to_excel(order_code, carrier, comment, dispatcher, issue_type, root_cause):
    response_manager = Evidencia_nezhod()
    response_manager.add_response(order_code, carrier, comment, dispatcher, issue_type, root_cause)
    response_manager.write_to_excel()


def get_cause(cause_delay, comment):
    cause = get_root_cause(cause_delay)
    # if cause == 'Iný dôvod':
    #     cause = comment
    return cause


def get_root_cause(case):
    switch = {
        'weather': 'Nepriaznivé počasie',
        'broken_truck': 'Pokazený kamión',
        'accident': 'Dopravná nehoda',
        'delay_loading': 'Zdržanie na predchádzajúcej nákladke',
        'delay_unloading': 'Zdržanie na predchádzajúcej výkladke',
        'driver_performance': 'Výkon vodiča',
        'traffic_situation': 'Dopravná situácia',
        'other': 'Iný dôvod',
    }

    return switch.get(case, None)

