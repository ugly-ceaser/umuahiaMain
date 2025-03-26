from django.shortcuts import render
from .settings import APP_NAME


def custom_error_404(request, exception):
    context = {
        "APP_NAME": APP_NAME,
        "status_code": 404,
    }
    return render(request, "404.html", context, status=404)


def custom_error_500(request):
    context = {
        "APP_NAME": APP_NAME,
        "status_code": 500,
    }
    return render(request, "500.html", context, status=500)
