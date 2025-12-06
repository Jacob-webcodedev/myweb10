import os
import requests
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)

MAILERSEND_API_KEY = os.getenv("MAILERSEND_API_KEY")

def check_api_key():
    if MAILERSEND_API_KEY:
        print("API Key check:", MAILERSEND_API_KEY[:6] + "..." + str(len(MAILERSEND_API_KEY)) + " chars total")
    else:
        raise ValueError("MAILERSEND_API_KEY not found in environment variables")

def send_test_email():
    url = "https://api.mailersend.com/v1/email"

    headers = {
        "Authorization": f"Bearer {MAILERSEND_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "from": {
            "email": "jacob.ho@jacobho.ca",
            "name": "Contact Form"
        },
        "to": [
            {
                "email": "jacob.ho@jacobho.ca",
                "name": "Jacob Ho"
            }
        ],
        "subject": "Test email using raw API",
        "text": "This is a plain text test email.",
        "html": "<p>This is a <strong>HTML</strong> test email.</p>"
    }

    response = requests.post(url, headers=headers, json=payload)
    print("status:", response.status_code)
    print("response:", response.text)

def send_contact_email(user_email, user_message):
    url = "https://api.mailersend.com/v1/email"

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
    if request.method == "POST":
        user_email = request.form.get("email")
        user_message = request.form.get("message")

        if send_contact_email(user_email, user_message):
            flash("✅ Your message was successfully sent!", "success")
        else:
            flash("❌ There was a problem sending your message. Please try again later.", "error")

        return redirect(url_for("index"))

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)