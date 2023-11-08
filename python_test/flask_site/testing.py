from flask import Flask, request, render_template
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 't402829@gmail.com'
app.config['MAIL_PASSWORD'] = ''# heslo od emailu

mail = Mail(app)

@app.route('/')
def index():
    #recipient_email = request.form['recipient_email']
    subject = 'Hello from your Flask app!'
    body = 'This is a test email sent from a Flask app.'

    msg = Message(subject, sender='t402829@gmail.com', recipients=["t402829@gmail.com"])
    msg.body = body

    try:
        mail.send(msg)
        return 'Email sent successfully!'
    except Exception as e:
        return 'Error sending email: ' + str(e)
    


    

if __name__ == '__main__':
    app.run(debug=True)
