from django.shortcuts import render, redirect, reverse
from django.views.generic import View, TemplateView, ListView, DetailView
from products.models import Product, Category
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Q


# Create your views here.
class HomePageView(TemplateView):
    def get(self,request):
        return render(request,'home.html',locals())

class ProductListView(View):
    def get(self, request):
        """显示列表页"""
        
        # 获取排序方式
        # sort=default 按照默认id排序
        # sort=price 按照商品价格排序
 
        sort = request.GET.get('sort')
        if sort == 'price':
            products = Product.objects.all().order_by('price')
        else:
            sort = 'default'
            products = Product.objects.all()
    

        # 对商品进行分页s
        paginator = Paginator(products, 2)

        page = request.GET.get('page')

        productsPage = paginator.get_page(page)

        # 获取商品的分类信息
        categories = Category.objects.all()

        

        


        # 组织上下文
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
        """显示列表页"""
        # 获取种类信息
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist :
            return redirect(reverse('products:index'))
        # 获取排序方式
        # sort=default 按照默认id排序
        # sort=price 按照商品价格排序
 
        sort = request.GET.get('sort')
        if sort == 'price':
            products = Product.objects.filter(category=category).order_by('price')
        else:
            sort = 'default'
            products = Product.objects.filter(category=category)
      

        # 对商品进行分页s
        paginator = Paginator(products, 2)

        page = request.GET.get('page')

        productsPage = paginator.get_page(page)


        # 获取商品的分类信息
        categories = Category.objects.all()

        

        


        # 组织上下文
        context = {
            'category': category,
            'productsPage': productsPage,
            'categories': categories,
            'products': products,
            'sort': sort,
            'page': page,
        }


        return render(request, 'category.html', context)

 
   

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "productDetail"
        return context


    
def searchProducts(request):
    if 'search' in request.GET and request.GET['search']:
        query = request.GET['search']
        categories = Category.objects.all()

        products = Product.objects.filter(Q(productName__icontains=query) & Q(id__icontains=query))
        

        # 对商品进行分页s
        paginator = Paginator(products, 2)

        page = request.GET.get('page')

        productsPage = paginator.get_page(page)
        
        return render(request, "searchProducts.html", locals())
    else:
        return HttpResponse("Please submit a search term.")