from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("checkout/", views.Checkout.as_view(), name="checkout"),
    path('orders/', views.OrdersView.as_view(), name="orders"),
    path("orderCommit/", views.OrderCommit, name="orderCommit"),
    path('orders/<str:PONumber>',views.OrderDetailView.as_view(), name='order_detail'),
    path("vendorShip/", views.vendorShip, name="vendorShip"),
    path("searchOrder/", views.searchOrder, name="searchOrder"),
    
]