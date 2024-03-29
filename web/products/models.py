from django.db import models

# Create your models here.
class Product(models.Model):
    productName = models.CharField(max_length=100)
    price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    ISBN = models.CharField(max_length=17)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    introduction = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='product')
    category = models.ForeignKey('Category', related_name="products", on_delete=models.CASCADE,)
    avgRating = models.FloatField(default=0)
    def __str__(self):
        return self.productName
    
    class Meta:
        indexes = [models.Index(fields=['productName', 'id']),]


class Category(models.Model):
    categoryName = models.CharField(max_length=50)


