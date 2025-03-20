from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from users.models import CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .utils import send_message
from umuahia_ireland.settings import APP_NAME, APP_URL
from django.template.loader import render_to_string
from .decorators import admin_required
from django.db import transaction
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from app.models import Minuites


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class MemberListView(AdminRequiredMixin, ListView):
    model = CustomUser
    template_name = "_admin/members.html"
    context_object_name = "users"

    def get_queryset(self):
        return CustomUser.objects.all().order_by("-date_joined")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_users"] = self.get_queryset().count()
        return context


# Create your views here.
@admin_required
def dashboard_member(request):
    if request.method == "POST":
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        first_name = request.POST.get("full_name").split()[0]
        last_name = request.POST.get("full_name").split()[-1]
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return redirect(reverse("admin:dashboard_members"))

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "User with this email already exists.")
            return redirect(reverse("admin:dashboard_members"))

        user = CustomUser.objects.create(
            email=email,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            position="member",
            password=make_password(password),  # Hash password before saving
        )

        messages.success(request, "User created successfully.")
        return redirect(reverse("admin:dashboard_members"))

    users = CustomUser.objects.all().order_by("-date_joined")[:5]
    return render(request, "_admin/dashboard.html", {"users": users})


@admin_required
def create_minutes(request):
    title = request.POST.get("title")
    date = request.POST.get("date")
    minutes = request.POST.get("minutes", "")

    if not title or not date:
        messages.error(request, "Title and Date are required.")
        return redirect(reverse("admin:minuites"))

    Minuites.objects.create(title=title, date=date, minuites=minutes)

    messages.success(request, "Minutes created successfully.")
    return redirect(reverse("admin:minuites"))


@admin_required
def dashboard_project(request):
    users = CustomUser.objects.all()
    total_users = CustomUser.objects.count()

    context = {"users": users, "total_users": total_users}

    return render(request, "_admin/dashboard-projects.html", context)


class MemberListView(AdminRequiredMixin, ListView):
    model = CustomUser
    template_name = "_admin/members.html"
    context_object_name = "users"

    def get_queryset(self):
        return CustomUser.objects.all().order_by("-date_joined")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_users"] = self.get_queryset().count()
        return context


class ProjectListView(AdminRequiredMixin, TemplateView):
    template_name = "_admin/projects.html"


class UserCreateView(AdminRequiredMixin, CreateView):
    model = CustomUser
    fields = ["firstName", "lastName", "email", "position"]
    template_name = "_admin/create_user.html"  # Create this template
    success_url = reverse_lazy("_admin:dashboard")

    def form_valid(self, form):
        user = form.save(commit=False)
        position = self.request.POST.get("position")

        is_admin = position == "admin"
        user.is_active = True
        user.is_staff = is_admin
        user.is_superuser = is_admin
        user.save()

        return super().form_valid(form)


class DeactivateUserView(AdminRequiredMixin, View):
    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        if user.is_active:
            user.is_active = False
            user.save()
            return redirect(reverse("_admin:dashboard"))
        return HttpResponse("User is already deactivated", status=400)


class ActivateUserView(AdminRequiredMixin, View):
    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        if not user.is_active:
            user.is_active = True
            user.save()
            return redirect(reverse("_admin:dashboard"))
        return HttpResponse("User is already active", status=400)


class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = CustomUser
    template_name = "_admin/user/delete.html"
    context_object_name = "user"

    def get_success_url(self):
        return reverse_lazy("_admin:dashboard")


class MinuitesListView(AdminRequiredMixin, ListView):
    model = Minuites
    template_name = "_admin/minuites.html"
    context_object_name = "minuites"

    def get_queryset(self):
        return Minuites.objects.all().order_by("-created_at")


class SettingsView(AdminRequiredMixin, TemplateView):
    template_name = "_admin/settings.html"


@admin_required
def change_password(request):
    if request.method == "POST":
        currentPassword = request.POST.get("current-password")
        newPassword = request.POST.get("new-password")
        confirmPassword = request.POST.get("new-password2")

        user = CustomUser.objects.get(id=request.user.id)

        if not user.check_password(currentPassword):
            messages.error(request, "Current password is incorrect!")
            return redirect(reverse("admin:settings"))

        if not newPassword == confirmPassword:
            messages.error(request, "Passwords do not match!")
            return redirect(reverse("admin:settings"))

        if newPassword == currentPassword:
            messages.error(request, "The new password cannot be your current password!")
            return redirect(reverse("admin:settings"))

        user.set_password(newPassword)
        user.save()
        messages.success(
            request,
            "Your password has been changed! You will be redirected to login again",
        )

        # Send welcome email
        # subject = f"Admin Password Changed"
        # context = {
        #     "APP_NAME": APP_NAME,
        #     "APP_URL": APP_URL,
        # }
        # body = render_to_string("email/admin/password-changed.html", context)
        # send_message(user, subject, "", body)

    return render(request, "_admin/settings.html")
