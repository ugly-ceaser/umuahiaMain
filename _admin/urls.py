from django.urls import path
from .views import (
    DashboardView,
    ProjectListView,
    MemberListView,
    ProjectListView,
    UserCreateView,
    UserUpdateView,
    UserDeactivateView,
    UserActivateView,
    UserDeleteView,
    MinuitesListView,
    CreateMinuitesView,
    SettingsView,
    ChangePasswordView,
    AdminResetUserPasswordView,
    EditMinuitesView,
    DeleteMinuitesView,
    CreateFinancialCheckbookView,
    EditFinancialCheckbookView,
    DeleteFinancialCheckbookView,
    FinancialCheckbookListView,
)

app_name = "admin"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("members/", MemberListView.as_view(), name="members"),
    path("create-user/", UserCreateView.as_view(), name="create_user"),
    path(
        "user/<uuid:user_id>/deactivate/",
        UserDeactivateView.as_view(),
        name="deactivate_user",
    ),
    path(
        "user/<uuid:user_id>/activate/",
        UserActivateView.as_view(),
        name="activate_user",
    ),
    path("user/<uuid:user_id>/delete/", UserDeleteView.as_view(), name="delete_user"),
    path(
        "user/<uuid:user_id>/reset-password/",
        AdminResetUserPasswordView.as_view(),
        name="reset_user_password",
    ),
    path("user/<uuid:user_id>/edit/", UserUpdateView.as_view(), name="edit_user"),
    path("minuites/", MinuitesListView.as_view(), name="minuites"),
    path("create-minuites/", CreateMinuitesView.as_view(), name="create_minutes"),
    path(
        "minuites/<uuid:minuites_id>/edit/",
        EditMinuitesView.as_view(),
        name="edit_minuites",
    ),
    path(
        "minuites/<uuid:minuites_id>/delete/",
        DeleteMinuitesView.as_view(),
        name="delete_minuites",
    ),
    path(
        "checkbook/", FinancialCheckbookListView.as_view(), name="financial_checkbook"
    ),
    path(
        "create-checkbook/",
        CreateFinancialCheckbookView.as_view(),
        name="create_checkbook",
    ),
    path(
        "checkbook/<uuid:checkbook_id>/edit/",
        EditFinancialCheckbookView.as_view(),
        name="edit_checkbook",
    ),
    path(
        "checkbook/<uuid:checkbook_id>/delete/",
        DeleteFinancialCheckbookView.as_view(),
        name="delete_checkbook",
    ),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
]
