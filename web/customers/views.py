from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from .forms import CustomerRegistrationForm, CustomerProfileAddForm
from django.contrib import messages
from .models import Customer
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

# Create your views here.
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.success(request,"Congratulations! User Register Successfully")
            username = self.request.POST["username"]
            password = self.request.POST.get("password", "default value")
            
            login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("profileAdd")     
            
        else:
            messages.warning(request,"Invalid Input Data")
        
        return render(request,'customerregistration.html',locals())


class ProfileAddView(View):
    def get(self,request):
        form = CustomerProfileAddForm()
        return render(request,'profileAdd.html',locals())
    def post(self,request):
        form = CustomerProfileAddForm(request.POST)
        if form.is_valid():
            user = request.user
            fullName = form.cleaned_data['fullName']
            phoneNum = form.cleaned_data['phoneNum']
            address = form.cleaned_data['address']
            

            reg = Customer(user=user, fullName=fullName, phoneNum=phoneNum, address=address)
            reg.save()
            messages.success(request, "Congratulations! Profile Save Successfully!")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'profileAdd.html',locals())

class CustomerProfileView(ListView):
    template_name = 'profile.html'
    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "MyProfile"
        return context
    
class CustomerProfileView(View):
    def get(self, request):
        profiles = Customer.objects.filter(user=request.user)

        context = {
            'profiles': profiles,
         }
        return render(request, 'profile.html', context)