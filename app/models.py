from django.db import models
import uuid


<<<<<<< HEAD




=======
>>>>>>> 42eaed3359a095090b0191334d151c696857daa3
# Create your models here.
class Minuites(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    title = models.CharField(max_length=100)
    date = models.DateField()
<<<<<<< HEAD
    minuites = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
=======
    minuites = models.FileField(upload_to="minuites/")
    created_at = models.DateTimeField(auto_now_add=True)
>>>>>>> 42eaed3359a095090b0191334d151c696857daa3
