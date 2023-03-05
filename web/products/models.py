from django.db import models

# Create your models here.
class Product(models.Model):
    productID = models.BigAutoField(primary_key=True)
    productName = models.CharField(max_length=100)
    price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    ISBN = models.CharField(max_length=17)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    introduction = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='product')
    category = models.ForeignKey('Category', related_name="products", on_delete=models.CASCADE,)
    avgRating = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    def __str__(self):
        return self.productName


class Category(models.Model):
    categoryID = models.BigAutoField(primary_key=True)
    categoryName = models.CharField(max_length=50)
    def __str__(self):
        return self.categoryName
    
class OrderItem(models.Model):
    productID = models.ForeignKey('Product', on_delete=models.CASCADE,)
    PONumber = models.ForeignKey('customers.Order', on_delete=models.CASCADE,)
    MyRate = models.DecimalField(default=0, max_digits=3, decimal_places=2)


