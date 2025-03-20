from django.db import models
import uuid


# Create your models here.
class Minuites(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    title = models.CharField(max_length=100)
    date = models.DateField()
    minuites = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
