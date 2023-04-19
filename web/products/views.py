from django.shortcuts import render, redirect, reverse
from django.views.generic import View, TemplateView, ListView, DetailView
from products.models import Product, Category
from order.models import OrderItem
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Q
from .forms import ProductsAddForm
from django.contrib import messages


# Create your views here.
class HomePageView(TemplateView):
    def get(self,request):
        return render(request,'home.html',locals())

class ProductListView(View):
    def get(self, request):
        sort = request.GET.get('sort')
        if sort == 'price':
            products = Product.objects.all().order_by('price')
        else:
            sort = 'default'
            products = Product.objects.all()
    
        paginator = Paginator(products, 6)

        page = request.GET.get('page')

        productsPage = paginator.get_page(page)

        categories = Category.objects.all()

        context = {
           
            'productsPage': productsPage,
            'categories': categories,
            'products': products,
            'sort': sort,
            'page': page,
        }

        return render(request, 'products.html', context)


    

class CategoryView(View):
    def get(self, request, category_id, page):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist :
            return redirect(reverse('products:index'))
 
        sort = request.GET.get('sort')
        if sort == 'price':
            products = Product.objects.filter(category=category).order_by('price')
        else:
            sort = 'default'
            products = Product.objects.filter(category=category)
      
        paginator = Paginator(products, 6)

        page = request.GET.get('page')

        productsPage = paginator.get_page(page)

        categories = Category.objects.all()

        context = {
            'category': category,
            'productsPage': productsPage,
            'categories': categories,
            'products': products,
            'sort': sort,
            'page': page,
        }

        return render(request, 'category.html', context)

 
   

class ProductDetailView(View):
   def get(self, request, pk):
        
        product = Product.objects.get(id=pk)
        items = OrderItem.objects.filter(product=product)

        avgRating = product.avgRating

        width = (avgRating / 5) * 100

        sumRating = 0
        j = 0
        for i in items:
            if i.myRate:
                sumRating = sumRating + i.myRate 
                j = j + 1

        if j != 0:
            avgRating = sumRating / j
            Product.objects.filter(id=pk).update(avgRating=avgRating)

        return render(request, 'product_detail.html', locals())


    
def searchProducts(request):
    if 'search' in request.GET and request.GET['search']:
        query = request.GET['search']
        categories = Category.objects.all()
        if query.isdigit():
            products = Product.objects.filter(Q(productName__icontains=query) | Q(id__exact=query))
        else:
            products = Product.objects.filter(Q(productName__icontains=query) )
  
        paginator = Paginator(products, 6)

        page = request.GET.get('page')

        productsPage = paginator.get_page(page)
        
        return render(request, "searchProducts.html", locals())
    else:
        return HttpResponse("Please submit a search term.")
    
class productsAddView(View):
    def get(self,request):
        form = ProductsAddForm()
        return render(request,'productsAdd.html',locals())
    def post(self,request):
        form = ProductsAddForm(request.POST, request.FILES)
        if form.is_valid():
            productName = form.cleaned_data['productName']
            price = form.cleaned_data['price']
            ISBN = form.cleaned_data['ISBN']
            author = form.cleaned_data['author']
            publisher = form.cleaned_data['publisher']
            introduction = form.cleaned_data['introduction']
            image = form.cleaned_data['image']
            category = form.cleaned_data['category']
            

            reg = Product(productName=productName, price=price, ISBN=ISBN, author=author, publisher=publisher, introduction=introduction, image=image, category=category)
            reg.save()
            pk = reg.pk
            
            return redirect("products:product_detail", pk = pk) 
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'productsAdd.html',locals())