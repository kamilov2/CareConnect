import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import python_version

def send_email(subject, message, recipients):
    server = 'smtp.yandex.com' 
    user = 'ivpplatform@yandex.com'
    password = 'efrlcevitfesgwit'
    sender = 'ivpplatform@yandex.com'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'IVP <' + sender + '>'
    msg['To'] = ', '.join(recipients)
    msg['Reply-To'] = sender
    msg['Return-Path'] = sender
    msg['X-Mailer'] = 'Python/' + (python_version())

    part_text = MIMEText(message, 'plain')
    msg.attach(part_text)

    try:
        mail = smtplib.SMTP_SSL(server)
        mail.login(user, password)
        mail.sendmail(sender, recipients, msg.as_string())
        print(recipients)
        mail.quit()
        print("Email sent successfully")
    except smtplib.SMTPException as e:
        print(f"Error: {e}")

