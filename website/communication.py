from flask import Blueprint, render_template, request
import secrets
import string
from . import db
import configparser
from website.models import Request, Response, User
from .excel import *
from flask_login.utils import _get_user
from .utils import *

communication = Blueprint('communication', __name__)



def generate_random_url() -> str:
    characters = string.ascii_letters + string.digits
    random_url = ''.join(secrets.choice(characters) for _ in range(20))
    return random_url


def read_language_file(file_path, lang_code):
    config = configparser.ConfigParser()
    config.read(file_path,encoding='utf-8')
    return config[lang_code]


def getLanguage(user, selected_lang):
    return 'SK' if isinstance(user, User) else selected_lang


@communication.route('/<chat_id>', methods=['GET', 'POST'])
def chat(chat_id):
    current_response = Response.query.filter(Response.response_id == chat_id).all()
    current_request = Request.query.filter(Request.response_id == chat_id).all()
    
    if not current_response:
        return render_template('communication.html', error = True)

    current_response = current_response[0]
    current_request = current_request[0]
    current_user = User.query.filter(current_request.user_id == User.id).first()
    order_code = current_request.order_code
    order = Order(order_code)

    if current_request.response:
        return render_template('communication.html', error = True)
   
    if request.method == 'POST' and 'languages' in request.form:
        selected_lang = request.form.get('languages')
    else:
        selected_lang = getLanguage(_get_user(), current_request.language)
    lang_data = read_language_file('website/nazvy.txt', selected_lang)
    
    if request.method == 'POST' and 'confirm_loading' in request.form or 'cause_delay' in request.form  or 'confirm_unloading' in request.form:
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

        carrier = order.carrier
        dispatcher = current_user.name
        email = current_user.email
        text = ""
            
        if loading:
            
            loaded_checkbox_value = request.form.get('loaded')
            if loaded_checkbox_value == 'loaded':
                text = "Nakládka je vykonaná"
            else:
                text = "Nakládka sa vykoná v dohodnutom čase"
                
        elif unloading:
            
            unloaded_checkbox_value = request.form.get('unloaded')
            
            if unloaded_checkbox_value == 'unloaded':
                text = "Vykládka je vykonaná"
            else:
                text = "Vykládka sa vykoná v dohodnutom čase"
                
        elif late_loading_value:

            write_response_to_excel(order_code, carrier, "Nakládka", get_cause(cause_delay), comment, dispatcher)

            text = f'Nakládka sa nevykoná v dohodnutom čase, predpokladaný dátum a čas príchodu:  {date} {time}' 

        elif late_unloading_value:
            
            write_response_to_excel(order_code, carrier, "Vykládka", get_cause(cause_delay), comment, dispatcher)

            text = f'Vykládka sa nevykoná v dohodnutom čase, predpokladaný dátum a čas príchodu:  {date} {time}' 

        current_request.response = True
        db.session.commit()

        try:
            send_email(f'Odpoveď na požiadavku k objednávke {order_code}', text, email)
            return render_template("after_response.html", **lang_data)
        except Exception:
            return render_template('communication.html', error = True)

        
        return render_template("after_response.html", **lang_data)
    
    return render_template('communication.html', **lang_data, selected_language = selected_lang,  error = False, chat_id=chat_id, res=current_response, req=current_request, order=order)


def write_response_to_excel(order_code, carrier, non_conformity, root_cause, comment, dispatcher):
    response_manager = Evidencia_nezhod()
    response_manager.add_response(order_code, carrier, non_conformity, root_cause, comment, dispatcher)
    response_manager.write_to_excel()


def get_cause(cause_delay):
    return get_root_cause(cause_delay)


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

