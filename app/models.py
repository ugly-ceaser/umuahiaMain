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
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    checkbook = models.FileField(upload_to="checkbooks/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
