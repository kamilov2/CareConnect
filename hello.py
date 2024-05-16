import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import python_version

server = 'server3.ahost.uz'
user = 'admin@careconnect.uz'
password = 'oILx6s-NE)kd'

recipients = ['jasurkamilov7279@gmail.com']
sender = 'admin@careconnect.uz'
subject = 'Тема сообщения '
text = 'Текст сообщения sdf sdf sdf sdaf <b>sdaf sdf</b> fg hsdgh <h1>f sd</h1> dfhjhgs sd gsdfg sdf'

msg = MIMEMultipart('alternative')
msg['Subject'] = subject
msg['From'] = 'Python script <' + sender + '>'
msg['To'] = ', '.join(recipients)
msg['Reply-To'] = sender
msg['Return-Path'] = sender
msg['X-Mailer'] = 'Python/' + (python_version())

part_text = MIMEText(text, 'plain')

msg.attach(part_text)

mail = smtplib.SMTP_SSL(server)
mail.login(user, password)
mail.sendmail(sender, recipients, msg.as_string())
mail.quit()
