from flask import Flask, render_template, request, url_for, redirect

from functions import *

app = Flask(__name__)
app.secret_key = b'hs8b9e256co648'

@app.route('/', methods = ['POST', 'GET'])
@app.route('/login/', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']

        if verify_user(mail, password):
            return redirect(url_for('main_page'))

    return render_template('login.html')

@app.route('/reset_password/', methods = ['POST', 'GET'])
def reset_password():
    return render_template('reset_password.html')

@app.route('/main_page/', methods = ['POST', 'GET'])
def main_page():
    return render_template('main_page.html')

@app.route('/user/', methods = ['POST', 'GET'])
def user():
    return render_template('user.html')
        

if __name__ == "__main__":
    app.run(debug=True)
