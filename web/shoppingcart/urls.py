from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("shoppingcart/", views.Cart, name="shoppingcart"),
    path("cartAdd/", views.CartAdd, name="cartAdd"),
    path('removecart/', views.remove_cart),
]