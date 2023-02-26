from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fullName = models.CharField(max_length=60)
    phoneNum = models.CharField(max_length=11)
    address = models.CharField(max_length=150)

    def __str__(self):
        return self.fullName


class Order(models.Model):
    PONumber = models.CharField(max_length=10)
    PurchaseDate = models.DateField()
    Status = models.CharField(max_length=60)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class ShoppingCart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ProductID = models.ForeignKey('products.Product',on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=0)
