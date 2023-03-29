from django.shortcuts import render, redirect
from django.views.generic import View
from customers.models import Customer
from shoppingcart.models import ShoppingCart
from order.models import OrderItem, Order
from django.db.models import Q
from django.http import JsonResponse
from django.db import transaction
from datetime import datetime
from order import models
from django.http import HttpResponse
import random


# Create your views here.
class Checkout(View):
    def get(self, request):
        user = request.user
        address = Customer.objects.filter(user=user)
        shoppingcart = ShoppingCart.objects.filter(user=user)
        PONumber = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 9999)) + str(user.id)
        totalamount = 0
        for p in shoppingcart:
            value = p.quantity * p.product.price
            totalamount = totalamount + value
        return render(request, 'checkout.html', locals())
    


def OrderCommit(request):
    totalamount = request.GET.get('totalamount')
    user = request.user
    PONumber = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 9999)) + str(user.id)
    shoppingcart = ShoppingCart.objects.filter(user=user)
    customer = Customer.objects.get(user=user)
    models.Order.objects.create(
        PONumber=PONumber,
        customer=customer,
        user=user,
        status="pending"
    ).save()
    order = Order.objects.get(PONumber=PONumber)
    for sc in shoppingcart:
        OrderItem(order=order,product=sc.product,price=sc.product.price).save()
        sc.delete()
    return redirect('order:order_detail', PONumber = PONumber)



class OrdersView(View):
    def get(self, request):
        """显示列表页"""
        user = request.user

        # 获取订单信息
        filter = request.GET.get('filter')
        if filter == 'current':
            orders = Order.objects.filter(Q(user=user) & (Q(status="pending") | Q(status="hold"))).order_by('-purchaseDate')
        elif filter == 'past':
            orders = Order.objects.filter(Q(user=user) & (Q(status="shipped") | Q(status="cancelled"))).order_by('-purchaseDate')
        elif filter == 'pending':
            orders = Order.objects.filter(status="pending").order_by('-purchaseDate')
        elif filter == 'hold':
            orders = Order.objects.filter(status="hold").order_by('-purchaseDate')
        elif filter == 'pastOrders':
            orders = Order.objects.filter(Q(status="shipped") | Q(status="cancelled")).order_by('-purchaseDate')
        elif filter == 'allVendor':
            orders = Order.objects.all().order_by('-purchaseDate')
        else:
            filter == 'all'
            orders = Order.objects.filter(user=user).order_by('-purchaseDate')

        total = []
        for o in orders:
            PONumber = o.PONumber
            order = Order.objects.get(PONumber=PONumber)
            orderitems = OrderItem.objects.filter(order=order)
            sum = 0
            for oi in orderitems:
                sum = sum + oi.price
            total.append(sum)
        orderZip = zip(orders,total)
            


      # 组织上下文
        context = {
           'orderZip': orderZip,
           'orders':orders,
        }

        return render(request, 'orders.html', context)
    



class OrderDetailView(View):
    def get(self, request, PONumber):
        """显示列表页"""

        # 获取订单信息
        filter = request.GET.get('filter')
        if filter == 'allVendor':
            orders = Order.objects.all().order_by('-purchaseDate')
        else:
            filter == 'all'
            orders = Order.objects.filter(user=request.user).order_by('-purchaseDate')
        
        
        order = Order.objects.get(PONumber=PONumber)
        
        orderitems = OrderItem.objects.filter(order=order)

        total = 0
        for oi in orderitems:
            value = oi.price
            total = total + value
        
        
        

      # 组织上下文
        context = {
           
            'order': order,
            'orderitems': orderitems,
            'total':total,
        }

        return render(request, 'order_detail.html', context)
    
def vendorShip(request):
    status = request.GET.get('status')
    PONumber = request.GET.get('PONumber')
    shipmentDate = datetime.now()
    Order.objects.filter(PONumber=PONumber).update(status=status,shipmentDate=shipmentDate)

    return redirect('order:order_detail', PONumber = PONumber)

def searchOrder(request):
    if 'search' in request.GET and request.GET['search']:
        query = request.GET['search']
        status = request.GET.get('status')
        orders = Order.objects.filter(Q(PONumber__icontains=query) & Q(status=status))
        total = []
        for o in orders:
            PONumber = o.PONumber
            order = Order.objects.get(PONumber=PONumber)
            orderitems = OrderItem.objects.filter(order=order)
            sum = 0
            for oi in orderitems:
                sum = sum + oi.price
            total.append(sum)
        orderZip = zip(orders,total)
        return render(request, "searchOrder.html", {'orders': orders, "search": query, "status": status, "orderZip": orderZip})
    else:
        return HttpResponse("Please submit a search term.")
