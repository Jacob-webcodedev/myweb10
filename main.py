import os
import requests
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)

# Secret key for flash messages
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# MailerSend API key from environment
MAILERSEND_API_KEY = os.getenv("MAILERSEND_API_KEY")


def check_api_key():
    """Quick sanity check for API key presence."""
    if MAILERSEND_API_KEY:
        print("API Key check:", MAILERSEND_API_KEY[:6] + "..." + str(len(MAILERSEND_API_KEY)) + " chars total")
    else:
        raise ValueError("MAILERSEND_API_KEY not found in environment variables")

def send_contact_email(user_email, user_message):
    """Send contact form submission via MailerSend API."""
    url = "https://api.mailersend.com/v1/email"

    headers = {
        "Authorization": f"Bearer {MAILERSEND_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "from": {"email": "jacob.ho@jacobho.ca", "name": "Website Contact"},
        "to": [{"email": "jacob.ho@jacobho.ca"}],
        "subject": "New contact form submission",
        "text": f"Message from {user_email}:\n\n{user_message}",
        "html": f"<p><strong>Message from {user_email}:</strong></p><p>{user_message}</p>",
        "reply_to": [{"email": user_email}]
    }

    response = requests.post(url, headers=headers, json=payload)
    print("status:", response.status_code)
    print("response:", response.text)

    return response.status_code == 202  # 202 Accepted = queued successfully


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
    check_api_key()  # sanity check at startup
    app.run(debug=True)