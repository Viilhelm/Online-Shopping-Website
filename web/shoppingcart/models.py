from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ShoppingCart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)