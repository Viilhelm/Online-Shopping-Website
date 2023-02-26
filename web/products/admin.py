from django.contrib import admin
from .models import Product,Category,OrderItem

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['productID','productName','price','category','ISBN','author','publisher','introduction','image','avgRating']
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['categoryID','categoryName']
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['productID','PONumber','MyRate']

