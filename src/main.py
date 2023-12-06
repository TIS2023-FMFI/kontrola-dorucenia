from flask import Flask, render_template, request, url_for, redirect, session
from functions import *

app = Flask(__name__)
app.secret_key = b'hs8b9e256co648'

@app.route('/', methods = ['POST', 'GET'])

@app.route('/login/', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']
    
        user = verify_user(mail, password)
        if user:
            session['admin'] = user[0][1]
            session['name'] = user[0][2]
            session['email'] = user[0][3]
            session['password'] = user[0][4]
            return redirect(url_for('main_page'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    if (len(session)>0):
        session.pop('admin')
        session.pop('name')
        session.pop('email')
        session.pop('password')
    return redirect(url_for('main_page'))

@app.route('/reset_password/', methods = ['POST', 'GET'])
def reset_password():
    return render_template('reset_password.html')

@app.route('/main_page/', methods = ['POST', 'GET'])
def main_page():
    if (len(session)>0):
        return render_template('main_page.html')
    return redirect(url_for('login'))

@app.route('/user/', methods = ['POST', 'GET'])
def user():
    if (len(session)>0):
        admin = bool(session.get('admin'))
        name = session.get('name')
        email = session.get('email')
        users = get_users()
        return render_template('user.html', name = name, email = email, admin = admin, users = users)
    return redirect(url_for('login'))

@app.route('/change_password_action', methods=['POST'])
def change_password_action():
    actual_password = request.form['actual_password']
    new_password = request.form['new_password']
    if(session.get('password') == actual_password):
        change_password(new_password, session.get('email'))
    return redirect(url_for('user'))

@app.route('/add_user_action', methods=['POST'])
def add_user_action():
    user_name = request.form['name']
    user_email = request.form['mail']
    user_password = request.form['password']
    if request.form.get('admin'):
        user_admin = 1
    else:
        user_admin = 0
    add_user(user_name,user_email,user_password, user_admin)
    return redirect(url_for('user'))

@app.route('/delete_user_action', methods=['POST'])
def delete_user_action():
    users_to_delete = request.form.getlist('users_to_delete')
    if users_to_delete:
        delete_user(users_to_delete)
    return redirect(url_for('user'))

if __name__ == "__main__":
    app.run(debug=True)





