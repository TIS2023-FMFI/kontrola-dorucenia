from flask import Blueprint, render_template, request, flash, jsonify, current_app
from flask_login import login_required, current_user
from flask_mail import Mail, Message
from . import db
import json
from .models import *
from .utils import *
import secrets
import datetime


requests = Blueprint('requests', __name__)


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
        new_request = Request(user_id=user_id, order_code=order_code, carrier_email=carrier_email, send_date=send_date, send_time=send_time, additional_message=additional_message, response=response )
        db.session.add(new_request)
        db.session.commit()
        request_data = {'id': new_request.id, 'order_code': new_request.order_code, 'carrier_email': new_request.carrier_email, 'send_date': new_request.send_date, 'send_time': json.dumps(new_request.send_time, default=str)}
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
            if not req.removeRequest():
                return jsonify({'success': False})
        return jsonify({'success': True})
    return jsonify({'success': False})

@requests.route('/send-request/', methods=['GET', 'POST'])
@login_required
def request_function(): # toto sa nemoze volat request, pretoze nastane konflikt s request.method ! 
    subject = 'Hello from your Flask app!'
    body = 'This is a test email sent from a Flask app.'

    msg = Message(subject, sender='t402829@gmail.com', recipients=["mattuss12@gmail.com"])
    msg.body = body

    try:
        Mail(current_app).send(msg)
        return 'Email sent successfully!'
    except Exception as e:
        return 'Error sending email: ' + str(e)
