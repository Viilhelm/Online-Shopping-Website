from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.HomePageView.as_view(), name='home'),
    path('products/', views.ProductListView.as_view(), name='products'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)