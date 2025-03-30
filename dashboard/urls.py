from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("minuites/", views.minuites, name="minuites"),
    path("checkbooks/", views.checkbooks, name="checkbooks"),
    path("update-profile/", views.update_profile, name="update_profile"),
    path("settings/", views.settings, name="settings"),
    path("change-password/", views.change_password, name="change_password"),
]
