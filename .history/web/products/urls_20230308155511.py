from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('home/', views.HomePageView.as_view(), name='home'),
    path(r'^products/(?P<page>\d+)$', views.ProductListView.as_view(), name='products'),
    path(r'^products/(?P<category_id>\d+)/(?P<page>\d+)$',views.CategoryView.as_view(), name='category'),
    path('produtcs/<int:pk>',views.ProductDetailView.as_view(), name='product_detail'),
    path("products/search/", views.SearchResultsView.as_view(), name="search_results"),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)