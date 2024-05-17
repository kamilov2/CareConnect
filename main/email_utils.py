from django.core.mail import send_mail


def send_email(subject, message, recipients):
    send_mail(subject, message, recipients)
    print("Email send succesfull ")
    
