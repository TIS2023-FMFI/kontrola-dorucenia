from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import secrets
import string

communication = Blueprint('communication', __name__)
conversations = {}

def generate_random_url():
    characters = string.ascii_letters + string.digits
    random_url = ''.join(secrets.choice(characters) for _ in range(20))
    return random_url

@communication.route('/chat/', methods=['GET', 'POST'])
@login_required
def chat():
    if request.method == 'POST':
        new_chat_id = generate_random_url()
        conversations[new_chat_id] = []
        return redirect(url_for('communication.create_chat', chat_id=new_chat_id))

    existing_chats = conversations.keys()

    return render_template('create_chat.html', existing_chats=existing_chats)


@communication.route('/<chat_id>', methods=['GET', 'POST'])
@login_required
def create_chat(chat_id):
    if chat_id not in conversations:
        return render_template('chat.html', chat_id='err', messages="Site not found!")

    if request.method == 'POST':
        message = request.form['message']
        conversations[chat_id].append({'sender': current_user.name, 'message': message})

    return render_template('chat.html', chat_id=chat_id, messages=conversations[chat_id])


@communication.route('/generate_new_chat', methods=['POST'])
@login_required
def generate_new_chat():
    new_chat_id = generate_random_url()
    conversations[new_chat_id] = []
    return redirect(url_for('communication.create_chat', chat_id=new_chat_id))
