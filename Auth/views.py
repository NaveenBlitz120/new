from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .forms import CreateUserForm
from django.shortcuts import render, redirect
from .decorators import unauthenticated_user,allowed_user


# Create your views here.
def login_page(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username = username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or Password is incorrect!!!')

    return render(request,'Auth/login.html')

def logout_page(request):
    logout(request)
    return redirect('login')    

@login_required(login_url='login')
def user_page(request):
    context={}
    return render(request,'Auth/user.html',context)



# @unauthenticated_user
@allowed_user(allowed_roles=['admin'])    
def register_page(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='admin')
            user.groups.add(group)
            messages.success(request,'Account was creater successfsully for '+username)
            return redirect('login')

    context= {'form':form}
    return render(request,'Auth/register.html',context)
