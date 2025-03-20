from django.core.mail import send_mail
from .settings import DEFAULT_EMAIL
from django.core.mail import send_mail

def send_message(subject, message, html_message, sender, reciepient):
    send_mail(
        subject,
        message,
        sender,
        [reciepient],
        html_message=html_message,
        fail_silently=False,
    )
    
def send_verification_email(user, subject, message, html_message=None):
    send_mail(
        subject,
        message,
        DEFAULT_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )
