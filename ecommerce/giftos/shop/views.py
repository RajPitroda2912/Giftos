from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import *
from .models import *

# Create your views here.
def home(request):
    product =Product.objects.all()[:10:3]
    data = {
        'product':product
    }
    return render(request,'home/index.html',data)

def contact(request):
    if request.method=='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact_data = Contact(name=name,email=email,phone=phone,message=message)
        contact_data.save()
        send_mail(
            "Thank YOU",
            "Thank you for your inquire",
            "rajpitroda2912@gmail.com",
            [email]
        )
        return redirect('shop:contactus')
    return render(request,'home/contact.html')

def shop(request):
    product =Product.objects.all()
    data = {
        'product':product
    }
    return render(request,'home/shop.html',data)

def testimonial(request):
    return render(request,'home/testimonial.html')

def why(request):
    return render(request,'home/why.html')

def Login(request):
    if request.method=='POST':
        form  = ReCaptcha(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            User = authenticate(email=email,password=password)
            if User is not None:
                login(request,User)
                return redirect('/')
            else:
                messages.error(request,"Email and Password is incorrect!")

    else:
        form = ReCaptcha()    
    return render(request,'login.html',{'form':form})

def signup(request):
    if request.method == 'POST':
        Register_form = RegisterUser(request.POST)
        if Register_form.is_valid():
            Register_form.save()
            return redirect('shop:login')
    else:
        Register_form = RegisterUser()
    return render(request,'signup.html', {'Register_form': Register_form})

def Logout(request):
    logout(request)
    return redirect('/')
