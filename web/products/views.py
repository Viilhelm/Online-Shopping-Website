from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from products.models import Product, Category

# Create your views here.
class HomePageView(TemplateView):
    def get(self,request):
        return render(request,'home.html',locals())

class ProductListView(ListView):
    model = Product
    template_name = 'products.html'
    paginate_by = 6
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "allProducts"
        return context
class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "categoryDetail"
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "productDetail"
        return context
