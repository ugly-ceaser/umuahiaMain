from django.urls import path
from .views import (
    user_login,
    user_register,
    user_logout,
    verificaton_email_sent,
    verify_account,
    resend_verification_email
)

app_name = "accounts"

urlpatterns = [
    path("login/", user_login, name="login"),
    path("register/<str:role>/", user_register, name="register"),
    path(
        "verification/email/sent/",
        verificaton_email_sent,
        name="verificaton_email_sent",
    ),
    path(
        "verification/email/resend/",
        resend_verification_email,
        name="resend_verification_email",
    ),
    path("verification/email/<str:token>/", verify_account, name="verify_account"),
    path("logout/", user_logout, name="logout"),
]
