import resend
import os
from dotenv import load_dotenv
from pathlib import Path


print("CWD:", Path.cwd())
print("Script:", Path(__file__).resolve())
print("Looking for .env at:", Path(__file__).parent / ".env")

load_dotenv()

key = os.getenv("RESEND_API_KEY")
print("RESEND_API_KEY repr:", repr(key))
print("RESEND_API_KEY length:", len(key) if key else "None")

resend.api_key = key

response = resend.Emails.send({
    "from": "Jacob Ho <jacob.ho@jacobho.ca>",
    "to": ["jacobho1583@gmail.com"],
    "subject": "Resend + IONOS DNS Test",
    "html": "<p>If you see this, your DNS is correct - hahaha From Trung 🎉</p>",
})

print(response)