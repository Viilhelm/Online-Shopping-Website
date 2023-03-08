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

# Create your views here.
class Checkout(View):
    def get(self, request):
        user = request.user
        address = Customer.objects.filter(user=user)
        shoppingcart = ShoppingCart.objects.filter(user=user)
        PONumber = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)
        totalamount = 0
        for p in shoppingcart:
            value = p.quantity * p.product.price
            totalamount = totalamount + value
        
        purchaseDate = datetime.now()
        purchaseDateString = purchaseDate.strftime("%m/%d/%Y, %H:%M:%S")
        return render(request, 'checkout.html', locals())



class OrdersView(View):
    def get(self, request):
        """显示列表页"""

        # 获取订单信息
        
        orders = Order.objects.filter(user=request.user)

        context = {
           
            'orders': orders,
            
        }

        for o in orders:
            PONumber = o.PONumber
            order = Order.objects.get(Q(PONumber=PONumber) & Q(user=request.user))
            orderitems = OrderItem.objects.filter(order=order)
            total = 0
            totalamount = []
            
            for oi in orderitems:
                value = oi.price
                total = total + value
            totalamount.append(total)
            


        
        

      # 组织上下文
        context = {
           
            'orders': orders,
            'totalamount':totalamount,
            
        }

        return render(request, 'orders.html', context)

def orderCommit(request):
    user = request.user
    PONumber = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)
    addressID = 1
    shoppingcart = ShoppingCart.objects.filter(user=user)
    customer = Customer.objects.get(id=1)
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
    return redirect('order:order_detail', kwargs={'PONumber' : PONumber})

class OrderDetailView(View):
    def get(self, request, PONumber):
        """显示列表页"""

        # 获取订单信息
        customer = Customer.objects.filter(id=1)
        
        order = Order.objects.get(Q(PONumber=PONumber) & Q(user=request.user))
        
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
            'customer':customer,
            
        }

        return render(request, 'order_detail.html', context)