from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.Checkout.as_view(), name="checkout"),
    path('orders/', views.OrdersView.as_view(), name="orders"),
    path("orderCommit/", views.OrderCommit, name="orderCommit"),
    path('orders/<str:PONumber>',views.OrderDetailView.as_view(), name='order_detail'),
    path("orderChange/", views.orderChange, name="orderChange"),
    path("searchOrder/", views.searchOrder, name="searchOrder"),
    path("report/", views.ReportView.as_view(), name="report"),
    path("searchDate/", views.searchDate, name="searchDate"),
    path("RRAdd/", views.RRAddView.as_view(), name="RRAdd"),
    path('submitRR/', views.submitRRView.as_view(), name='submitRR'),
    path('RRAgain/', views.RRAgainView.as_view(), name='RRAgain'),
    
]