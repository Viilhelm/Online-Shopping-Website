from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from products.models import Product, Category

# Create your views here.
class HomePageView(TemplateView):
    def get(self,request):
        return render(request,'home.html',locals())

class ProductListView(ListView):
    model = Product
    template_name = 'products.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "allProducts"
        return context