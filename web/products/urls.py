from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.ProductListView.as_view(), name='products'),
    path('home/', views.ProductListView.as_view(), name='home'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path(r'^products/(?P<category_id>\d+)/(?P<page>\d+)$',views.CategoryView.as_view(), name='category'),
    path('produtcs/<int:pk>',views.ProductDetailView.as_view(), name='product_detail'),
    path("searchProducts/", views.searchProducts, name="searchProducts"),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)