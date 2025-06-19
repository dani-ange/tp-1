from email.mime.text import MIMEText
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json
def send_email(zip_path):
    sender = os.environ["EMAIL_SENDER"]
    receiver = os.environ["EMAIL_RECEIVER"]
    password = os.environ["EMAIL_PASSWORD"]
    smtp_server = os.environ["SMTP_SERVER"]
    smtp_port = int(os.environ["SMTP_PORT"])

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    
    # Attach the email body as plain text
    msg.attach(MIMEText(body, "plain"))

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
    try:
        with open("results.json", "r") as f:
            results = json.load(f)
        subject = "Model Training & Deployment Successful"
        body = (
            f"Model trained and evaluated successfully.\n"
            f"Results:\nAccuracy: {results['accuracy']:.4f}\n"
            f"F1 Score: {results['f1_score']:.4f}"
        )
        zip_path = "bundle.zip"  # <-- Set your zip file name here
    except Exception as e:
        subject = "Model Training or Deployment Failed"
        body = f"An error occurred:\n{e}"
        zip_path = None
    send_email("bundle.zip")
