import smtplib
from email.mime.text import MIMEText

EMAIL = "youremail@gmail.com"
PASSWORD = "yourpassword"

def send_email(to, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to

    # Dummy email print for school demo (disable actual send)
    print(f"[DUMMY EMAIL] To: {to}, Subject: {subject}\n{body}\n")
