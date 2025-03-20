from django.urls import path
from . import views

app_name = "admin"

urlpatterns = [
    path("", views.dashboard_member, name="dashboard_members"),
    path("projects/", views.dashboard_project, name="dashboard_projects"),
    path("members/", views.MemberListView.as_view(), name="members"),
    path("projects/", views.ProjectListView.as_view(), name="projects"),
    path("create-user/", views.UserCreateView.as_view(), name="create_user"),
    path(
        "user/<int:user_id>/deactivate/",
        views.DeactivateUserView.as_view(),
        name="deactivate_user",
    ),
    path(
        "user/<int:user_id>/activate/",
        views.ActivateUserView.as_view(),
        name="activate_user",
    ),
    path("user/<pk>/delete/", views.UserDeleteView.as_view(), name="delete_user"),
    path("minuites/", views.MinuitesListView.as_view(), name="minuites"),
    path("create-minuites/", views.create_minutes, name="create_minutes"),
    path("settings/", views.SettingsView.as_view(), name="settings"),
    path("change-password/", views.change_password, name="change-password"),
]
