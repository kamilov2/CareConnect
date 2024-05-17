import smtplib
from django.core.mail import send_mail

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import python_version



def send_email(subject, message, recipients):
    server = 'smtp.yandex.com'
    port = 465
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
        mail = smtplib.SMTP_SSL(server, port)
        mail.login(user, password)
        mail.sendmail(sender, recipients, msg.as_string())
        print(recipients)
        mail.quit()
        print("Email sent successfully")
        
    except smtplib.SMTPAuthenticationError:
        print("Authentication failed. Check username/password.")
    except smtplib.SMTPConnectError:
        print("Failed to connect to the server. Check server/port.")
    except smtplib.SMTPRecipientsRefused:
        print("All recipients were refused. Check recipient email addresses.")
    except smtplib.SMTPSenderRefused:
        print("The sender address was refused. Check sender email address.")
    except smtplib.SMTPDataError:
        print("The SMTP server refused to accept the message data.")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
