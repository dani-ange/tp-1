import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(zip_path):
    sender = os.environ["EMAIL_SENDER"]
    receiver = os.environ["EMAIL_RECEIVER"]
    password = os.environ["EMAIL_PASSWORD"]
    smtp_server = os.environ["SMTP_SERVER"]
    smtp_port = int(os.environ["SMTP_PORT"])

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "📦 Model and Documentation Delivery"

    # Attach the zip
    part = MIMEBase('application', "octet-stream")
    with open(zip_path, "rb") as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(zip_path)}"')
    msg.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver.split(','), msg.as_string())

if __name__ == "__main__":
    send_email("bundle.zip")
