from django.shortcuts import render, redirect, get_object_or_404
from .decorators import validation_required
from django.urls import reverse
from users.models import CustomUser
from django.contrib import messages
from app.models import Minuites
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse


@validation_required
def dashboard(request):
    return render(request, "_user/profile.html")


def minuites(request):
    # Fetch all the minutes from the database
    minutes_list = Minuites.objects.all()

    if request.method == "POST" and "download_minute" in request.POST:
        minute_id = request.POST.get("minute_id")
        minute = get_object_or_404(Minuites, id=minute_id)

        # Generate PDF dynamically
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 800, f"Title: {minute.title}")

        p.setFont("Helvetica", 12)
        p.drawString(100, 780, f"Date: {minute.date.strftime('%B %d, %Y')}")

        # Add minutes content with text wrapping
        p.setFont("Helvetica", 11)
        text = minute.minuites
        text_lines = text.split("\n")
        y_position = 760
        for line in text_lines:
            p.drawString(100, y_position, line)
            y_position -= 20

        p.showPage()
        p.save()

        buffer.seek(0)
        response = HttpResponse(buffer, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{minute.title}.pdf"'
        return response

    # Render the page with the minutes list
    return render(request, "_user/minuites.html", {"minutes": minutes_list})


@validation_required
def settings(request):
    return render(request, "_user/settings.html")


@validation_required
def update_profile(request):
    if request.method == "POST":
        # Handle form submission
        first_name = request.POST.get("fullName").split()[0]
        last_name = request.POST.get("fullName").split()[-1]
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        location = request.POST.get("location")
        about = request.POST.get("about")

        # Save changes to the user profile
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone_number = phone
        user.location = location
        user.about = about
        user.save()

        return redirect(reverse("user:dashboard"))

    return render(request, "_user/update-profile.html")


@validation_required
def change_password(request):
    if request.method == "POST":
        currentPassword = request.POST.get("current-password")
        newPassword = request.POST.get("new-password")
        confirmPassword = request.POST.get("new-password2")

        user = CustomUser.objects.get(id=request.user.id)

        if not user.check_password(currentPassword):
            messages.error(request, "Current password is incorrect!")
            return redirect(reverse("user:settings"))

        if not newPassword == confirmPassword:
            messages.error(request, "Passwords do not match!")
            return redirect(reverse("user:settings"))

        if newPassword == currentPassword:
            messages.error(request, "The new password cannot be your current password!")
            return redirect(reverse("user:settings"))

        user.set_password(newPassword)
        user.save()

        messages.success(
            request,
            "Your password has been changed! You will be redirected to login again",
        )
        return redirect(reverse("user:settings"))
