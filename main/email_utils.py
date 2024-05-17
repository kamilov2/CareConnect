import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import python_version

def send_email(subject, message, recipients):
    server = 'smtp.yandex.com'
    port = 465  # Порт для SMTP_SSL
    user = 'ivpplatform@yandex.com'
    password = 'efrlcevitfesgwit'
    sender = 'ivpplatform@yandex.com'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f'IVP <{sender}>'
    msg['To'] = ', '.join(recipients)
    msg['Reply-To'] = sender
    msg['Return-Path'] = sender
    msg['X-Mailer'] = f'Python/{python_version()}'

    part_text = MIMEText(message, 'plain')
    msg.attach(part_text)

    try:
        print("Connecting to the SMTP server...")
        mail = smtplib.SMTP_SSL(server, port)
        mail.set_debuglevel(1)  # Включить вывод отладочной информации для подключения SMTP
        mail.login(user, password)
        mail.sendmail(sender, recipients, msg.as_string())
        mail.quit()
        print("Email sent successfully")
    except smtplib.SMTPConnectError as e:
        print(f"SMTP connection error: {e}")
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP authentication error: {e}")
    except smtplib.SMTPException as e:
        print(f"SMTP error: {e}")
    except Exception as e:
        print(f"General error: {e}")
