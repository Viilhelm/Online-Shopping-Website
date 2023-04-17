from django.contrib import admin
from .models import Order,OrderItem

# Register your models here.
@admin.register(Order)
class OrderlAdmin(admin.ModelAdmin):
    list_display = ['PONumber','purchaseDate','status','customer','user', 'vendor']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id','product','order','price','myRate','myComment','commentAgain','RRDate']
