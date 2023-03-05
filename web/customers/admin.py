from django.contrib import admin
from .models import Customer,Order,ShoppingCart

# Register your models here.
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['user','fullName','phoneNum','address']
@admin.register(Order)
class OrderlAdmin(admin.ModelAdmin):
    list_display = ['PONumber','PurchaseDate','Status','user']
@admin.register(ShoppingCart)
class ShoppingCartrlAdmin(admin.ModelAdmin):
    list_display = ['user','ProductID','Quantity']



