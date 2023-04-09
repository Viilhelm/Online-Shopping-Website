from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.Checkout.as_view(), name="checkout"),
    path('orders/', views.OrdersView.as_view(), name="orders"),
    path("orderCommit/", views.OrderCommit, name="orderCommit"),
    path('orders/<str:PONumber>',views.OrderDetailView.as_view(), name='order_detail'),
    path("vendorShip/", views.vendorShip, name="vendorShip"),
    path("vendorCancel/", views.vendorCancel, name="vendorCancel"),
    path("vendorHold/", views.vendorHold, name="vendorHold"),
    path("searchOrder/", views.searchOrder, name="searchOrder"),
    path("report/", views.ReportView.as_view(), name="report"),
    path("searchDate/", views.searchDate, name="searchDate"),
    path("RRAdd/", views.RRAddView.as_view(), name="RRAdd"),
    path('rating/', views.rating),
]