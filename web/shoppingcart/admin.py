from django.contrib import admin
from .models import ShoppingCart

# Register your models here.
@admin.register(ShoppingCart)
class ShoppingCartrlAdmin(admin.ModelAdmin):
    list_display = ['user','product','quantity']
