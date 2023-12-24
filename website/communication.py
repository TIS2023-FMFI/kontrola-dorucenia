from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import secrets
import string
from collections import OrderedDict


communication = Blueprint('communication', __name__)
conversations = OrderedDict()

def generate_random_url() -> str:
    characters = string.ascii_letters + string.digits
    random_url = ''.join(secrets.choice(characters) for _ in range(20))
    existing_urls = set(conversations.keys())
    while random_url in existing_urls: # Ak by sa nahodou vytvorila url, ktora uz existuje
        random_url = ''.join(secrets.choice(characters) for _ in range(20))
    conversations[random_url] = []
    return random_url

def getConversations() -> OrderedDict:
    return conversations

def deleteConversation(index : int) -> bool:
    if len(conversations) < index+1:
        return False
    toDelete = conversations.items()[index]
    conversations.pop(toDelete, None)
    return True 

@communication.route('/<chat_id>', methods=['GET', 'POST'])
def chat(chat_id):
    if chat_id not in conversations:
        return render_template('chat.html', chat_id='err', messages="Site not found!")

    if request.method == 'POST':
        message = request.form['message']
        conversations[chat_id].append({'sender': current_user.name, 'message': message})

    return render_template('SK.html', chat_id=chat_id, messages=conversations[chat_id])

