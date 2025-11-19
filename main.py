from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
import secrets

secure_key = secrets.token_hex(16)
print(secure_key)


import smtplib
from email.message import EmailMessage

print("Start!")



app = Flask(__name__)
app.secret_key = '7eac3d1bf882df7c7e3a65f43f7c7352'  # Needed for flashing messages


# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'jacobpython1583@gmail.com'
app.config['MAIL_PASSWORD'] = 'sxiw kxdm sgyg iunf'  # Use Gmail App Password

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/experience')
def experience():
    return render_template("experience.html")

@app.route('/education')
def education():
    return render_template("education.html")

@app.route("/details")
def details():
    return render_template("aboutme.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form.get('email')
        message = request.form['message']

        try:
            msg = Message(subject=f'New message from {name}',
                          sender=email,
                          recipients=['jacobpython1583@gmail.com'],
                          body=f"{email} has sent you this: \n {message}")
            mail.send(msg)
            flash(f'Message sent successfully by {email}')
        except Exception as e:
            print("Email failed:", e)
            flash('Failed to send message.')
        return redirect('/')

    return render_template('/')


if __name__ == '__main__':
    app.run(debug=True)