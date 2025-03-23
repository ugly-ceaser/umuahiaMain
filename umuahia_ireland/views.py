
from umuahia_ireland.settings import Admin_Email
from django.core.mail import send_mail
from umuahia_ireland.settings import DEFAULT_EMAIL

from .utils import send_verification_email
from django.contrib.auth.models import User
from django.http import JsonResponse  # Add this import


EMAIL_DIR = "../templates/registration/email"




def send_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        message = request.POST.get('message')

         # Compose the email message
        subject = f"New Contact Form Submission from {name} {surname}"
        body = f"""
        Name: {name}
        Surname: {surname}
        Email: {email}
        Message: {message}
        """
        admin_email = Admin_Email
        
        
        print("here")
        
        

        try:
            
            # dummy_user = User(email=admin_email)
            # send_verification_email(dummy_user, subject, body, None)
            send_mail(
                subject,
                body,
                email,
                [admin_email],
                html_message=None,
                fail_silently=False,
            )
           
        
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})
