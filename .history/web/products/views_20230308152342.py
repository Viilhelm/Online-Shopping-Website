from django.shortcuts import render, redirect, reverse
from django.views.generic import View, TemplateView, ListView, DetailView
from products.models import Product, Category
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.http import HttpResponse



# Create your views here.
class HomePageView(TemplateView):
    def get(self,request):
        return render(request,'home.html',locals())

class ProductListView(View):
    def get(self, request,  page):
        """显示列表页"""
        
        # 获取排序方式
        # sort=default 按照默认id排序
        # sort=price 按照商品价格排序
 
        sort = request.GET.get('sort')
        if sort == 'price':
            products = Product.objects.all().order_by('price')
      
        else:
            sort = 'default'
            products = Product.objects.all().order_by('-id')

        # 对商品进行分页s
        paginator = Paginator(products, 1)

        # 获取第page页的内容
        try:
            page = int(page)
        except Exception as e:
            page = 1 
        if page > paginator.num_pages:
            page = 1

        # 获取第page页的paginator.page实例对象
        products_page = paginator.page(page)

        # todo: 进行页码控制， 页面上最多显示5个页面
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        # 获取商品的分类信息
        categories = Category.objects.all()

        

        


        # 组织上下文
        context = {
           
            'products_page': products_page,
            'categories': categories,
            'products': products,
            'sort': sort,
            'pages': pages,
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
            products = Product.objects.filter(category=category).order_by('-id')

        # 对商品进行分页s
        paginator = Paginator(products, 1)

        # 获取第page页的内容
        try:
            page = int(page)
        except Exception as e:
            page = 1
        if page > paginator.num_pages:
            page = 1

        # 获取第page页的paginator.page实例对象
        products_page = paginator.page(page)

        # todo: 进行页码控制， 页面上最多显示5个页面
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        # 获取商品的分类信息
        categories = Category.objects.all()

        

        


        # 组织上下文
        context = {
            'category': category,
            'products_page': products_page,
            'categories': categories,
            'products': products,
            'sort': sort,
            'pages': pages,
        }


        return render(request, 'category.html', context)

 
   

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "productDetail"
        return context


    
