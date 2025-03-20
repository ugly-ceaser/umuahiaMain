from django.contrib import admin
from .models import CustomUser


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = [
        "first_name",
        "last_name",
        "email",
        "date_joined",
        "last_login",
        "is_active",
    ]


admin.site.register(CustomUser, CustomUserAdmin)
