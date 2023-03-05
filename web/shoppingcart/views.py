from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import JsonResponse
from products.models import Product
from shoppingcart.models import ShoppingCart
from django_redis import get_redis_connection
from django.db.models import Q

# Create your views here.
def CartAdd(request):
    user = request.user
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    ShoppingCart(user=user, product=product).save()
    return redirect('/shoppingcart')

def Cart(request):
    user = request.user
    shoppingcart = ShoppingCart.objects.filter(user=user)
    totalamount = 0
    for p in shoppingcart:
        value = p.quantity * p.product.price
        totalamount = totalamount + value
    
    return render(request, 'cartAdd.html',locals())

def pluscart(request):
    if request.method == 'GET':
        product_id = request.GET.get('product_id')
        product = Product.objects.get(id=product_id)
        c = ShoppingCart.objects.get(Q(product=product) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        shoppingcart = ShoppingCart.objects.filter(user=user)
        totalamount = 0
        for p in shoppingcart:
            value = p.quantity * p.product.price
            totalamount = totalamount + value
        data = {
            'quantity':c.quantity,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def minuscart(request):
    if request.method == 'GET':
        product_id = request.GET.get('product_id')
        product = Product.objects.get(id=product_id)
        c = ShoppingCart.objects.get(Q(product=product) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        shoppingcart = ShoppingCart.objects.filter(user=user)
        totalamount = 0
        for p in shoppingcart:
            value = p.quantity * p.product.price
            totalamount = totalamount + value
        data = {
            'quantity':c.quantity,
            'totalamount':totalamount
        }
        return JsonResponse(data)
  
def remove_cart(request):
    if request.method == 'GET':
        product_id = request.GET.get('product_id')
        product = Product.objects.get(id=product_id)
        c = ShoppingCart.objects.get(Q(product=product) & Q(user=request.user))
        c.delete()
        user = request.user
        shoppingcart = ShoppingCart.objects.filter(user=user)
        totalamount = 0
        for p in shoppingcart:
            value = p.quantity * p.product.price
            totalamount = totalamount + value
        data = {
            'quantity':c.quantity,
            'totalamount':totalamount
        }
        return JsonResponse(data)
  