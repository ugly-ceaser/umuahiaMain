from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.views.generic import ListView, TemplateView, View
from django.contrib.auth.mixins import UserPassesTestMixin
from users.models import CustomUser
from app.models import Minuites, FinancialCheckbook
from django.core.exceptions import ValidationError


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class DashboardView(AdminRequiredMixin, ListView):
    model = CustomUser
    template_name = "_admin/dashboard.html"
    context_object_name = "users"

    def get_queryset(self):
        return CustomUser.objects.all().order_by("-date_joined")[:5]


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


class UserCreateView(AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            full_name = request.POST.get("full_name", "").strip()
            position = request.POST.get("position")
            password = request.POST.get("password")

            if not full_name:
                raise ValidationError("Full name is required")
            if not password:
                raise ValidationError("Password is required")

            name_parts = full_name.split()
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

            CustomUser.objects.create(
                email=request.POST.get("email"),
                first_name=first_name,
                last_name=last_name,
                position=position,
                is_active=True,
                is_staff=(position == "admin"),
                is_superuser=(position == "admin"),
                password=make_password(password),
            )

            return redirect("admin:dashboard")
        except ValidationError:
            return redirect("admin:dashboard")  # Optionally, add a message
        except Exception:
            return redirect("admin:dashboard")


class UserUpdateView(AdminRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        return render(request, "_admin/edit_user.html", {"user": user})

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.email = request.POST.get("email", user.email)
        user.position = request.POST.get("position", user.position)
        user.save()
        messages.success(request, "User details updated successfully.")
        return redirect("admin:members")


class UserDeactivateView(AdminRequiredMixin, View):
    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        if user.is_active:
            user.is_active = False
            user.save()
        return redirect("admin:members")


class UserActivateView(AdminRequiredMixin, View):
    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        if not user.is_active:
            user.is_active = True
            user.save()
        return redirect("admin:members")


class UserDeleteView(AdminRequiredMixin, View):
    def post(self, request, user_id):
        get_object_or_404(CustomUser, id=user_id).delete()
        return redirect("admin:members")


class MinuitesListView(AdminRequiredMixin, ListView):
    model = Minuites
    template_name = "_admin/minuites.html"
    context_object_name = "minuites"

    def get_queryset(self):
        return Minuites.objects.all().order_by("-created_at")


# Edit Minutes view
class EditMinuitesView(AdminRequiredMixin, View):
    def get(self, request, minuites_id):
        minuite = get_object_or_404(Minuites, id=minuites_id)
        return render(request, "_admin/edit_minuites.html", {"minuite": minuite})

    def post(self, request, minuites_id):
        minuite = get_object_or_404(Minuites, id=minuites_id)
        minuite.title = request.POST.get("title", minuite.title)
        minuite.date = request.POST.get("date", minuite.date)
        # If a new file is uploaded, update it; otherwise keep existing file
        if "minuites" in request.FILES:
            minuite.minuites = request.FILES.get("minuites")
        minuite.save()
        messages.success(request, "Minutes updated successfully.")
        return redirect("admin:minuites")


# Delete Minutes view
class DeleteMinuitesView(AdminRequiredMixin, View):
    def post(self, request, minuites_id):
        minuite = get_object_or_404(Minuites, id=minuites_id)
        minuite.delete()
        messages.success(request, "Minutes deleted successfully.")
        return redirect("admin:minuites")


class CreateMinuitesView(AdminRequiredMixin, View):
    def post(self, request):
        title = request.POST.get("title")
        date = request.POST.get("date")
        minuites_file = request.FILES.get("minuites")

        print(title, date, minuites_file)

        if not (title and date and minuites_file):
            messages.error(request, "All fields are required.")
            return redirect("admin:minuites")

        Minuites.objects.create(title=title, date=date, minuites=minuites_file)
        messages.success(request, "Minutes created successfully.")
        return redirect("admin:minuites")


class SettingsView(AdminRequiredMixin, TemplateView):
    template_name = "_admin/settings.html"


class ChangePasswordView(AdminRequiredMixin, View):
    def post(self, request):
        current_password = request.POST.get("current-password")
        new_password = request.POST.get("new-password")
        confirm_password = request.POST.get("new-password2")

        user = request.user

        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect!")
            return redirect("admin:settings")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("admin:settings")

        if new_password == current_password:
            messages.error(request, "The new password cannot be your current password!")
            return redirect("admin:settings")

        user.set_password(new_password)
        user.save()
        messages.success(
            request,
            "Your password has been changed! You will be redirected to login again",
        )
        return redirect("admin:settings")


class AdminResetUserPasswordView(AdminRequiredMixin, View):
    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        new_password = request.POST.get("new-password")
        confirm_password = request.POST.get("confirm-password")

        if not new_password or not confirm_password:
            messages.error(request, "Both password fields are required!")
            return redirect("admin:edit_user", user_id=user.id)

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("admin:edit_user", user_id=user.id)

        user.set_password(new_password)
        user.save()
        messages.success(
            request, f"Password for {user.email} has been reset successfully!"
        )
        return redirect("admin:edit_user", user_id=user.id)


class FinancialCheckbookListView(AdminRequiredMixin, ListView):
    model = FinancialCheckbook
    template_name = "_admin/financial_checkbook.html"
    context_object_name = "checkbook_list"

    def get_queryset(self):
        return FinancialCheckbook.objects.all().order_by("-created_at")


# Create Financial Checkbook Entry
class CreateFinancialCheckbookView(AdminRequiredMixin, View):
    def post(self, request):
        transaction_type = request.POST.get("transaction_type")
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        description = request.POST.get("description")
        checkbook_file = request.FILES.get("checkbook")

        print(transaction_type, amount, date, description, checkbook_file)

        if not (transaction_type and amount and date and checkbook_file):
            messages.error(
                request, "Transaction type, amount, date and checkbook are required."
            )
            return redirect("admin:financial_checkbook")

        FinancialCheckbook.objects.create(
            transaction_type=transaction_type,
            amount=amount,
            date=date,
            description=description,
            checkbook=checkbook_file,
        )

        messages.success(request, "Financial checkbook entry added successfully.")
        return redirect("admin:financial_checkbook")


# Edit Financial Checkbook Entry
class EditFinancialCheckbookView(AdminRequiredMixin, View):
    def get(self, request, checkbook_id):
        checkbook_entry = get_object_or_404(FinancialCheckbook, id=checkbook_id)
        return render(
            request,
            "_admin/edit_financial_checkbook.html",
            {"checkbook": checkbook_entry},
        )

    def post(self, request, checkbook_id):
        checkbook_entry = get_object_or_404(FinancialCheckbook, id=checkbook_id)
        checkbook_entry.transaction_type = request.POST.get(
            "transaction_type", checkbook_entry.transaction_type
        )
        checkbook_entry.amount = request.POST.get("amount", checkbook_entry.amount)
        checkbook_entry.description = request.POST.get(
            "description", checkbook_entry.description
        )
        checkbook_entry.checkbook = request.POST.get(
            "checkbook", checkbook_entry.checkbook
        )
        checkbook_entry.save()
        messages.success(request, "Financial checkbook entry updated successfully.")
        return redirect("admin:financial_checkbook")


# Delete Financial Checkbook Entry
class DeleteFinancialCheckbookView(AdminRequiredMixin, View):
    def post(self, request, checkbook_id):
        checkbook_entry = get_object_or_404(FinancialCheckbook, id=checkbook_id)
        checkbook_entry.delete()
        messages.success(request, "Financial checkbook entry deleted successfully.")
        return redirect("admin:financial_checkbook")
