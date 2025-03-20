from users.models import CustomUser
from app.models import Minuites


def global_counts(request):
    return {
        "total_users": CustomUser.objects.count(),
        # "total_projects": Project.objects.count(),
        "total_minutes": Minuites.objects.count(),
    }
