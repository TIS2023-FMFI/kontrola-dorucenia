from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import secrets
import string
from collections import OrderedDict
from . import db

from website.models import Request, Response, Chat

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

    if request.method == 'POST':

        #vsetky if-ka trackuju to, co sa zakliklo vo formulari SK.html- mohlo sa zakliknut len to ze sa uskutocnila nakladka,
        # a zaroven aj vsetko naraz preto to je takto vyclenene

        loaded_checkbox_value = request.form.get('loaded')
        if loaded_checkbox_value == 'loaded' and not current_response.loaded:
            add_new_chat("Nákladka sa vykoná v dohodnutom čase.", current_response)
            current_response.load()

        unloaded_checkbox_value = request.form.get('unloaded')
        if unloaded_checkbox_value == 'unloaded' and not current_response.unloaded and current_response.loaded:
            add_new_chat("Výkladka sa vykoná v dohodnutom čase.", current_response)
            current_response.unload()

        cause_delay = request.form.get('cause_delay')
        if cause_delay:
            current_response.set_root_cause(cause_delay)

        comment = request.form.get('message')
        if comment:
            current_response.set_comment(comment)

        date = request.form.get('date')
        time = request.form.get('time')

        late_loading_value = request.form.get('late_loading')
        if late_loading_value:
            if not current_response.loaded:
                current_response.set_loading_date(date)
                current_response.set_loading_time(time)
                current_response.set_delay_loading(True)

                cause = get_cause(cause_delay, comment)

                add_new_chat("Vozidlo bude meškať na nákladku z dôvodu " + cause + ".", current_response)
                add_new_chat("Predpokladaný čas nákladky: " + date + " " + time, current_response)

        late_unloading_value = request.form.get('late_unloading')
        if late_unloading_value:
            if not current_response.unloaded and current_response.loaded:
                current_response.set_unloading_date(date)
                current_response.set_unloading_time(time)
                current_response.delay_unloading = True

                cause = get_cause(cause_delay, comment)

                add_new_chat("Vozidlo bude meškať na výkladku z dôvodu " + cause + ".", current_response)

                add_new_chat("Predpokladaný čas výkladky: " + date + " " + time, current_response)

    all_chat = Chat.query.filter(Chat.response_id == current_response.response_id).all()
    return render_template('SK.html', chat_id=chat_id, res=current_response, req=current_request, chat=all_chat)


def get_cause(cause_delay, comment):
    cause = get_root_cause(cause_delay)
    if cause == 'Iný dôvod':
        cause = comment
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


def add_new_chat(text, current_response):
    new_chat = Chat(string=text, response_id=current_response.response_id)
    db.session.add(new_chat)
    db.session.commit()
