from umuahia_ireland.settings import DEFAULT_EMAIL
from django.core.mail import send_mail


def send_message(user, subject, message, html_message):
    send_mail(
        subject,
        message,
        DEFAULT_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )
