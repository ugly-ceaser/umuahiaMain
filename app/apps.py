from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from umuahia_ireland.config import (
    SUPERUSER_EMAIL,
    SUPERUSER_PASSWORD,
)


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"  # Replace with your actual app name

    def ready(self):
        """Connects the post_migrate signal to create an admin user after migrations."""
        post_migrate.connect(create_default_admin, sender=self)


def create_default_admin(sender, **kwargs):
    """Creates a default admin account if one doesn't exist after migrations."""
    from django.db.utils import OperationalError, ProgrammingError

    User = get_user_model()

    try:

        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                email=SUPERUSER_EMAIL, password=SUPERUSER_PASSWORD, is_verified=True
            )
            print(f"✅ Admin account created: {SUPERUSER_EMAIL}")
        else:
            print("✅ Admin account already exists. Skipping creation.")

    except (OperationalError, ProgrammingError):
        print("⚠️ Database not ready yet. Skipping admin creation.")
