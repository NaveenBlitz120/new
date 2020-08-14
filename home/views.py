from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')

def homefun(request):
    return render(request,"home/loginpage.html")

def map(request):
    return render(request , "home/sample.html")
