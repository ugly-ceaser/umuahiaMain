from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from functools import wraps
from django.urls import reverse
from django.contrib.auth import login, get_user_model, logout
from django.contrib.auth.hashers import make_password
from users.models import CustomUser
from django.contrib import messages
from umuahia_ireland.settings import APP_NAME, APP_URL
from django.template.loader import render_to_string
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .utils import send_verification_email
from django.db import transaction
from django.utils.timezone import now
from datetime import timedelta

EMAIL_DIR = "../templates/registration/email"


def validation_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_staff:
                return redirect(reverse("admin:dashboard_members"))
            return redirect(reverse("user:dashboard"))
        # If all checks pass, call the view function
        return view_func(request, *args, **kwargs)

    return _wrapped_view


# Function based handler views
@validation_required
def user_register(request, role):
    """
    Handles user registration. This function retrieves user data from POST request,
    checks if the email already exists, ensures passwords match, and creates a new user.
    If successful, logs in the user and sends a welcome email.

    Parameters:
    request (HttpRequest): The HTTP request object containing POST data.

    Returns:
    HttpResponse: Redirects to the registration page on failure or the dashboard on success.
    """

    # Redirect already logged-in users
    if request.user.is_authenticated:
        return redirect(reverse("dashboard:dashboard"))

    if request.method == "POST":
        try:
            # Retrieve data from POST request
            phone_number = request.POST.get("phone")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirmPassword = request.POST.get("password2")

            # Hash the password
            hashed_password = make_password(password)

            # Check if email already exists
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, message="Email already exists!")

            # Check if phone number already exists
            if CustomUser.objects.filter(phone_number=phone_number).exists():
                messages.error(
                    request,
                    message="Phone number is already linked to a different account!",
                )
                return render(request, "regist`ration/register.html")

            # Check if passwords match
            if password != confirmPassword:
                messages.error(request, message="Passwords do not match!")
                return render(request, "registration/register.html")

            with transaction.atomic():
                # Create a new user
                new_user = CustomUser.objects.create(
                    email=email,
                    phone_number=phone_number,
                    password=hashed_password,
                    is_superuser=role == "admin",
                    is_staff=role == "admin",
                )

                new_user.generate_verification_token()

                # Send welcome email
                subject = f"🎉 Welcome to {APP_NAME} {new_user.email}!"
                verification_link = (
                    f"{APP_URL}/auth/verification/email/{new_user.verification_token}/"
                )
                context = {
                    "APP_NAME": APP_NAME,
                    "APP_URL": APP_URL,
                    "VERIFICATION_URL": verification_link,
                    "user": new_user,
                }
                body = render_to_string(f"{EMAIL_DIR}/welcome.html", context)
                send_verification_email(new_user, subject, "", body)

                login(request, new_user)

            return redirect(reverse("accounts:verificaton_email_sent"))

        except Exception as e:
            print(e)
            messages.error(
                request, message=f"An error occurred during registration! {e}"
            )
    return render(request, "registration/register.html")


def resend_verification_email(request):
    if request.method == "POST":
        user = request.user

        if user.is_verified:
            messages.success(request, "Your account is already verified.")
            return redirect(reverse("dashboard:dashboard"))

        # Generate new token
        user.generate_verification_token()

        # Prepare and send email
        subject = f"📧 Verify Your {APP_NAME} Account"
        verification_link = (
            f"{APP_URL}/auth/verification/email/{user.verification_token}/"
        )
        context = {
            "APP_NAME": APP_NAME,
            "APP_URL": APP_URL,
            "VERIFICATION_URL": verification_link,
            "user": user,
        }
        body = render_to_string(f"{EMAIL_DIR}/welcome.html", context)
        send_verification_email(user, subject, "", body)

        messages.success(request, "A new verification email has been sent.")
        return redirect(reverse("accounts:verificaton_email_sent"))

    return redirect(reverse("dashboard:dashboard"))


def verificaton_email_sent(request):
    return render(request, "registration/verification_email_sent.html")


# Verify Account View
def verify_account(request, token):
    try:
        with transaction.atomic():
            user = get_object_or_404(CustomUser, verification_token=token)

            # Optional: Check if the token has expired (24-hour window)
            if user.token_created_at and now() - user.token_created_at > timedelta(
                hours=24
            ):
                messages.error(
                    request,
                    "Verification link has expired. Please request a new verification email.",
                )
                return render(request, "registration/verification_failed.html")

            # Mark the user as verified
            user.verification_token = None
            user.token_created_at = None
            user.is_verified = True
            user.save()

            messages.success(request, "Your email has been successfully verified!")
            return render(request, "registration/verification_success.html")

    except Exception as e:
        # Catch any unexpected errors and show a message
        messages.error(
            request, f"An error occurred during verification. Please try again later!"
        )
        return render(request, "registration/verification_failed.html")


@validation_required
def user_login(request):
    """
    Handles user login. This function retrieves the email and password from the POST request,
    checks if the user exists and the password is correct, and logs in the user if successful.

    Parameters:
    request (HttpRequest): The HTTP request object containing POST data.

    Returns:
    HttpResponse: Renders the login page on failure or redirects to the dashboard on success.
    """
    # Redirect already logged-in users
    if request.user.is_authenticated:
        return redirect(reverse("user:dashboard"))

    if request.method == "POST":
        try:
            # Retrieve data from POST request
            email = request.POST.get("email")
            password = request.POST.get("password")

            print(f"Email: {email} Password: {password}")

            # Get the user by email
            user = get_object_or_404(CustomUser, email=email)
            if user is not None and user.check_password(password):
                login(request, user)  # Log the user in
                if user.is_superuser or user.is_staff:
                    return redirect(reverse("admin:dashboard_members"))
                else:
                    return redirect(reverse("user:dashboard"))
            else:
                messages.error(request, message="Invalid email or password!")
        except Http404:
            messages.error(request, message="Invalid email or password!")
        except Exception as e:
            messages.error(request, message=f"An error occurred! {e}")

    # Render login page with messages in case of any failure
    return render(request, "registration/login.html")


@login_required
def user_logout(request):
    """
    Handles user logout. Logs the user out and redirects to the home page.

    Parameters:
    request (HttpRequest): The HTTP request object.

    Returns:
    HttpResponse: Redirects to the home page after logging out.
    """
    logout(request)  # Log the user out
    return redirect(reverse("app:home_page"))
