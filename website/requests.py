from flask import Blueprint, request, jsonify, url_for
from flask_login import login_required, current_user
from . import db
import json
from .models import *
from .utils import *
from .excel import *
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .communication import generate_random_url


requests = Blueprint('requests', __name__)
scheduler = BackgroundScheduler(timezone="Europe/Bratislava")


@requests.route('/create_request_action', methods=['POST'])
@login_required
def create_request():
    if request.method == 'POST':
        data = request.get_json()
        user_id = current_user.id
        order_code = data.get('order_code')
        carrier_email = data.get('carrier_email')
        datelist = data['send_date'].split('-')
        send_date = datetime.date(int(datelist[0]), int(datelist[1]), int(datelist[2]))
        timelist = data['send_time'].split(':')
        send_time = datetime.time(int(timelist[0]), int(timelist[1]))
        additional_message = data.get('additional_message')
        response = False
        new_chat_id = generate_random_url()
        main_page_url = url_for('views.home', _external=True)
        website_link = f'{main_page_url}/{new_chat_id}'
        lang = getLanguage(order_code, carrier_email)
        if lang in ('CZ', 'SK'):
            lang = 'SK'
        else:
            lang = 'EN'
        new_request = Request(user_id=user_id, order_code=order_code, carrier_email=carrier_email,
                              send_date=send_date, send_time=send_time, additional_message=additional_message, response=response, response_id  = new_chat_id, language = lang)
        db.session.add(new_request)
        db.session.commit()

        new_response = Response(request_id = new_request.id, response_id = new_chat_id)
        db.session.add(new_response)
        db.session.commit()

        request_data = {'id': new_request.id, 'order_code': new_request.order_code, 'carrier_email': new_request.carrier_email, 'send_date': new_request.send_date, 'send_time': json.dumps(new_request.send_time, default=str)}
        scheduled_date = datetime.datetime(int(datelist[0]), int(datelist[1]), int(datelist[2]), int(timelist[0]), int(timelist[1]), 0)
        scheduler.add_job(send_email, 'date', args=['Communication',  f'{website_link}\n{additional_message}', carrier_email], run_date=scheduled_date)
        if not scheduler.running:
            scheduler.start()
        return jsonify({'success': True, 'request': request_data})
    return jsonify({'success': False})



@requests.route('/get_requests', methods=['GET'])
@login_required
def get_requests():
    requests = Request.query.all()
    request_data = [{'id': req.id, 'order_code': req.order_code, 'carrier_email': req.carrier_email, 'send_date': req.send_date, 'send_time': req.send_time} for req in requests]
    return jsonify(request_data)

@requests.route('/delete_requests', methods=['POST'])
@login_required
def delete_requests():
    if request.method == 'POST':
        data = request.get_json()
        request_ids_to_delete = data.get('requests_to_delete')
        for request_id in request_ids_to_delete:
            req = find_request(int(request_id))
            res = Response.query.filter(Response.request_id == request_id).all()[0]
            if not req.removeRequest():
                return jsonify({'success': False})
            if not res.removeResponse():
                return jsonify({'success': False})

        return jsonify({'success': True})
    return jsonify({'success': False})
