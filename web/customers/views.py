from django.shortcuts import render
from django.views import View
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from .models import Customer

# Create your views here.
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'customerregistration.html',locals())

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            fullName = form.cleaned_data['fullName']
            phoneNum = form.cleaned_data['phoneNum']
            address = form.cleaned_data['address']

            reg = Customer(user=user, fullName=fullName, phoneNum=phoneNum, address=address)
            reg.save()
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'profile.html',locals())