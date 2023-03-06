from django.urls import path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("checkout/", views.Checkout.as_view(), name="checkout"),
    path('orders/', views.OrdersView.as_view(), name="orders"),
    path("orderCommit/", views.orderCommit, name="orderCommit"),
    re_path(r'^orders/(?P<PONumber>\w+)$',views.OrderDetailView.as_view(), name='order_detail'),
    
]