# email_utils.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(recipient_email, subject, body):
    sender_email = "shieldcyber59@gmail.com"
    sender_password = "rvkj tlmv pzid koio"

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender_email, sender_password)
        session.sendmail(sender_email, recipient_email, message.as_string())
        session.quit()
        print("✅ Email sent successfully to", recipient_email)
    except Exception as e:
        print("❌ Email send failed:", e)
