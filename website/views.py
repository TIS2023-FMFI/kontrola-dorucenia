from flask import Blueprint, render_template, request, flash, jsonify, current_app, redirect, url_for
from flask_login import login_required, current_user
from flask_mail import Mail, Message
from . import db
import json
from flask_bcrypt import Bcrypt
import pandas as pd
from .models import *
from .utils import *
from .excel import *
import secrets

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method== 'POST':
        order_code = request.form.get('order_code')
        order = Order(order_code)
        if order.exist():
            carrier = Carrier(order.carrier)
            if carrier.exist():
                email_addresses = []
                for dispatcher in carrier.dispatchers:
                    email_addresses.append(dispatcher.email)
                return render_template("order.html", user=current_user, order_code=order_code, email_addresses=email_addresses)
            flash('Incorrect carrier code', category='error')
        else:
             flash('Incorrect order code', category='error')

    requests_without_response = Request.query.filter(Request.response == False)
    return render_template("order_search.html", user=current_user, requests=requests_without_response)

@views.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_data = [{'id': user.id, 'name': user.name, 'email': user.email, 'admin': user.admin} for user in users]
    return jsonify(user_data)

@views.route('/add_user_action', methods=['POST'])
def add_user():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        email = data.get('mail')
        password = Bcrypt().generate_password_hash(data.get('password'))
        admin = data.get('admin', False)
        new_user = User(name=name, email=email, password=password, admin=admin)
        db.session.add(new_user)
        db.session.commit()
        user_data = {'id': new_user.id, 'name': new_user.name, 'email': new_user.email, 'admin': new_user.admin}
        return jsonify({'success': True, 'user': user_data})
    
    return jsonify({'success': False})
    
@views.route('/change_password_action', methods=['POST'])
def change_password():
     if request.method == 'POST':
        data = request.get_json()
        current_password = data.get('password')
        if Bcrypt().check_password_hash(current_user.password, current_password):
            new_password = Bcrypt().generate_password_hash(data.get('new_password'))
            current_user.changePassword(new_password)
            return jsonify({'success': True})
        return jsonify({'success': False})


@views.route('/reset_password/', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        selected_user = find_user(None, email)
        if not selected_user:
            return render_template("reset_password.html", user=current_user, message="Email does not exist!")
        new_password = secrets.token_urlsafe(12)
        hashed_pass = Bcrypt().generate_password_hash(new_password)
        try:
            send_email("New password", f'Your new password is {new_password}')
            selected_user.changePassword(hashed_pass)
            return render_template("login.html", user=current_user, message = "The Password has been sent to your email!")
        except Exception:
            return render_template("reset_password.html", user=current_user, message = "Error while sending a message!")
    return render_template("reset_password.html", user=current_user)

@views.route('/delete_users', methods=['POST'])
def delete_users():
    if request.method == 'POST':
        data = request.get_json()
        user_ids_to_delete = data.get('users_to_delete')
        for user_id in user_ids_to_delete:
            user = find_user(int(user_id))
            if not user.removeUser():
                return jsonify({'success': False})
        return jsonify({'success': True})
    return jsonify({'success': False})

    
@views.route('/user/', methods=['GET', 'POST'])
@login_required
def user():
    users_from_db = []
    if current_user.admin:
        users_from_db = User.query.all()
        users_from_db.remove(current_user)
    return render_template("user_info.html", user=current_user, users = users_from_db)

@views.route('/order/', methods=['GET', 'POST'])
@login_required
def order():
    return render_template("order.html",  user=current_user, order_code=order_code, email_addresses=email_addresses)

