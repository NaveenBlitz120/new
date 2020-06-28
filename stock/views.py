from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import *
from .forms import Create,Update
from .filters import myFilter
from django.contrib.auth.decorators import login_required
from Auth.decorators import unauthenticated_user,allowed_user,admin_only




# Create your views here.
@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def stockfun(request):

    medi_obj = medicine.objects.all()
    #comp_obj = company.objects.all()
    myfilter = myFilter(request.GET,queryset=medi_obj)
    medi_obj= myfilter.qs
    context ={ 'medi':medi_obj , 'filter':myfilter  }
    return render(request, 'stock/search.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def create(request):

    form = Create()

    context = {'form':form,}
    if request.method == 'POST':
        #print('printing POST:',request.POST)
        form = Create(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/stock')

    return render(request,'stock/forms.html',context)

@login_required(login_url='login')
@admin_only
def updates(request,pk):

    order = medicine.objects.get(id=pk)
    form = Update(instance=order)
    if request.method == 'POST':
        form = Update(request.POST,instance = order)
        if form.is_valid():
            form.save()
            return redirect('/stock')


    context = {'form':form}
    return render(request,'stock/forms.html',context)

@login_required(login_url='login')
@admin_only
def delete(request,pk):

    order = medicine.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/stock')

    context = {'item':order}
    return render(request,'stock/delete.html',context)
