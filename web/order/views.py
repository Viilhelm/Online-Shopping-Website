from django.shortcuts import render, redirect
from django.views.generic import View
from customers.models import Customer
from shoppingcart.models import ShoppingCart
from order.models import OrderItem, Order
from products.models import Product
from django.db.models import Q
from datetime import datetime, timedelta
from order import models
from django.http import HttpResponse
import random
from django.http import JsonResponse
from .forms import ReviewForm
from django.contrib import messages


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
        status="pending",
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
           'orders': orders,
           'filter': filter,
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

def vendorCancel(request):
    status = request.GET.get('status')
    PONumber = request.GET.get('PONumber')
    cancelDate = datetime.now()
    Order.objects.filter(PONumber=PONumber).update(status=status,cancelDate=cancelDate)

    return redirect('order:order_detail', PONumber = PONumber)

def vendorHold(request):
    status = request.GET.get('status')
    PONumber = request.GET.get('PONumber')
    Order.objects.filter(PONumber=PONumber).update(status=status)

    return redirect('order:order_detail', PONumber = PONumber)

def searchOrder(request):
    if 'search' in request.GET and request.GET['search']:
        query = request.GET['search']
        status = request.GET.get('status')
        
        orders = Order.objects.filter(Q(PONumber__icontains=query))

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
        return render(request, "searchOrder.html", {"orders": orders, "filter": filter, "search": query, "status": status, "orderZip": orderZip})
    else:
        return HttpResponse("Please submit a search term.")
    
class ReportView(View):
    def get(self, request):
        orders = Order.objects.filter(purchaseDate__lte=datetime.now(), purchaseDate__gte=datetime.now() + timedelta(days=-30))
        items = OrderItem.objects.filter(order__in=orders)

        pName = []
        for item in items:           
            pName.append((item.product.productName,item.product.price))
        
        dic = {}
        for p in pName:
            dic[p] = dic.get(p, 0) + 1

        sort = sorted(dic.items(), key=lambda kv: kv[1], reverse=True)

        length = len(items)
        
        total = 0
        for k, v in dic.items():
            total = total + k[1] * v

        best = []
        first = sort[0][1]
        for i in sort:
            if i[1] == first:
                best.append(i)

        

      # 组织上下文
        context = {
           'items': items,
           'dic': dic,
           'sort': sort,
           'length': length,
           'total': total,
           'best': best,
        }

        return render(request, 'report.html', context)
    
def searchDate(request):
    if 'datetimepicker1' in request.GET and request.GET['datetimepicker1'] and 'datetimepicker2' in request.GET and request.GET['datetimepicker2']:
        datetimepicker1 = request.GET['datetimepicker1']
        datetimepicker2 = request.GET['datetimepicker2']
        
        orders = Order.objects.filter(purchaseDate__lte=datetimepicker2, purchaseDate__gte=datetimepicker1)
        items = OrderItem.objects.filter(order__in=orders)

        pName = []
        for item in items:           
            pName.append((item.product.productName,item.product.price))
        
        dic = {}
        for p in pName:
            dic[p] = dic.get(p, 0) + 1

        sort = sorted(dic.items(), key=lambda kv: kv[1], reverse=True)

        length = len(items)
        
        total = 0
        for k, v in dic.items():
            total = total + k[1] * v
        
        best = []
        first = sort[0][1]
        for i in sort:
            if i[1] == first:
                best.append(i)
        

        context = {
            'items': items,
            'dic': dic,
            'sort': sort,
            'length': length,
            'total': total,
            'best': best,
            'datetimepicker1': datetimepicker1,
            'datetimepicker2': datetimepicker2,
        }

        return render(request, "searchDate.html", context)
    else:
        return HttpResponse("Please select a date range.")
    

    
class RRAddView(View):
    def get(self,request):
        form = ReviewForm()
        PONumber = request.GET.get('PONumber')
        item_id = request.GET.get('item_id')
        order = Order.objects.get(PONumber=PONumber)
        item = OrderItem.objects.get(id=item_id)

        
        return render(request,'RRAdd.html', locals())
    
class RRAllAddView(View):
    def get(self, request):
        form = ReviewForm()
        PONumber = request.GET.get('PONumber')

        order = Order.objects.get(PONumber=PONumber)
        orderitems = OrderItem.objects.filter(order=order)

        return render(request,'RRAllAdd.html', locals())

   

    

def submitRR(request):
    if request.method == 'POST':
        PONumber = request.POST.get('PONumber')
        item_id = request.POST.get('item_id') 


        product_id = OrderItem.objects.get(id=item_id).product_id

        items = OrderItem.objects.filter(product_id=product_id)

        avgRating = Product.objects.get(id=product_id).avgRating



          
        form = ReviewForm(request.POST)
        if form.is_valid():
            myRate = form.cleaned_data['myRate']
            myComment = form.cleaned_data['myComment']

            OrderItem.objects.filter(id=item_id).update(myRate=myRate,myComment=myComment)

            j = 0
            for items in items:
                if items.myRate:
                    j = j + 1

            sumRating = avgRating * (j - 1) + myRate
            avgRating = sumRating / j

            Product.objects.filter(id=product_id).update(avgRating=avgRating)
            

            messages.success(request, 'Thank you! Your review has been submitted.')
            return redirect('/home')
        



