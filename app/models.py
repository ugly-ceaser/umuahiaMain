from django.db import models
import uuid


# Create your models here.
class Minuites(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    title = models.CharField(max_length=100)
    date = models.DateField()
    minuites = models.FileField(upload_to="minuites/")
    created_at = models.DateTimeField(auto_now_add=True)


class FinancialCheckbook(models.Model):
    TRANSACTION_TYPES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.CharField(max_length=255)
    checkbook = models.FileField(upload_to="checkbooks/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
