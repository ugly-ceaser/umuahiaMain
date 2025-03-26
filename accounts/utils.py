from django.utils import timezone
from umuahia_ireland.settings import DEFAULT_EMAIL
from django.core.mail import send_mail


def send_verification_email(user, subject, message, html_message=None):
    send_mail(
        subject,
        message,
        DEFAULT_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )
