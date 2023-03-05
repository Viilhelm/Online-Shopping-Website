from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from .forms import LoginForm

urlpatterns = [
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('profile/', views.CustomerProfileView.as_view(), name='profile'),
    path('profileAdd/', views.ProfileAddView.as_view(), name='profileAdd'),
   

]