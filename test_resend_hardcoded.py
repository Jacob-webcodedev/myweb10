import resend
import os
from dotenv import load_dotenv

load_dotenv()


resend.api_key = "re_LZ2hUoNQ_KeTNan7Bo7h8LuX7aRMRvvxi"

response = resend.Emails.send({
    "from": "Jacob Ho <jacob.ho@jacobho.ca>",
    "to": ["jacobho1583@gmail.com"],
    "subject": "Resend + IONOS DNS Test",
    "html": "<p>If you see this, your DNS is correct - hahaha From Trung 🎉</p>",
})

print(response)