from django.shortcuts import render
from umuahia_ireland.config import APP_NAME


# Create your views here.
def home(request):
    return render(request, "index.html")
