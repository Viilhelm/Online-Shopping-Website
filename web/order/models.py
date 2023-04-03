from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

ORDER_STATUS_CHOICES = (
        ('pending', 'pending'),
        ('shipped', 'shipped'),
        ('hold', 'hold'),
        ('cancelled', 'cancelled'),
        
    )


# Create your models here.
class Order(models.Model):
    PONumber = models.CharField(max_length=30, primary_key=True)
    purchaseDate = models.DateTimeField(default=datetime.now)
    status = models.CharField(default=ORDER_STATUS_CHOICES[0][0], choices=ORDER_STATUS_CHOICES, max_length=20)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    shipmentDate = models.DateTimeField(null = True)
    cancelDate = models.DateTimeField(null = True)
    vendor = models.ForeignKey('vendors.Vendor',on_delete=models.CASCADE, default=4)
    customer = models.ForeignKey('customers.Customer',on_delete=models.CASCADE)

class OrderItem(models.Model):
    
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE,)
    price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    myRate = models.IntegerField(default=5)
    myComment = models.CharField(max_length=1000)

    class Meta:
        unique_together = ("product","order")