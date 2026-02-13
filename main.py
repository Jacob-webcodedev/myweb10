import os
import requests
from flask import Flask, render_template, request, flash, redirect, url_for, session
from google_auth_oauthlib.flow import Flow


app = Flask(__name__)

# Secret key for flash messages
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# MailerSend API key from environment
RESEND_API_KEY = os.getenv("RESEND_API_KEY")


def check_api_key():
    """Quick sanity check for API key presence."""
    if RESEND_API_KEY:
        print("API Key check:", RESEND_API_KEY[:6] + "..." + str(len(RESEND_API_KEY)) + " chars total")
    else:
        raise ValueError("RESEND_API_KEY not found in environment variables")

def send_contact_email(user_email, user_message):
    """Send contact form submission via Resend API."""
    url = "https://api.resend.com/emails"

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "from": {"email": "jacob.ho@jacobho.ca", "name": "Website Contact"},
        "to": [{"email": "jacobho1583@gmail.com"}],
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

@app.route("/authorize")
def authorize():
    # Step 3 code: start OAuth flow
    flow = Flow.from_client_secrets_file(
        "credentials.json",
        scopes=["https://www.googleapis.com/auth/drive.readonly"],
        redirect_uri=url_for("oauth2callback", _external=True)
    )
    auth_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(auth_url)

@app.route("/oauth2callback")
def oauth2callback():
    # Step 3 code: handle callback
    flow = Flow.from_client_secrets_file(
        "credentials.json",
        scopes=["https://www.googleapis.com/auth/drive.readonly"],
        redirect_uri=url_for("oauth2callback", _external=True)
    )
    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials
    session["credentials"] = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes
    }
    return "Authorization complete!"


if __name__ == '__main__':
    check_api_key()  # sanity check at startup
    app.run(debug=True)