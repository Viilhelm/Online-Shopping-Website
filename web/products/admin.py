from django.contrib import admin
from .models import Product,Category

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','productName','price','category','ISBN','author','publisher','introduction','image','avgRating']
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','categoryName']


