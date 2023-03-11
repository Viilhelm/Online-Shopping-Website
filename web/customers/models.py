from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    fullName = models.CharField(max_length=60)
    phoneNum = models.CharField(max_length=11)
    address = models.CharField(max_length=150)

    def __str__(self):
        return self.fullName
    
