from django.urls import path
from . import views

urlpatterns = [
    path("shoppingcart/", views.Cart, name="shoppingcart"),
    path("cartAdd/", views.CartAdd, name="cartAdd"),
    path('removecart/', views.remove_cart),
]