from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from .models import *
from .forms import *
from django.contrib.auth.models import User
from .filters import *

def get_total_of_this_item(quantity,price_billed):
	return price_billed*quantity

def createinvoice(request):
	flag=1
	bill_total=0
	user = request.user
	error_query = invoice.objects.filter(user = user,invoice_complete=False)
	error_query_order = Order.objects.filter(invoice_id__in = error_query,complete = False)
	if (error_query) != []:
		error_query.delete()
	if (error_query_order) != []:
		for i in range(len(error_query_order)):
			error_query_order[i].delete()
	orderformset = orderitemFormset()
	form = Create_invoice()
	context = { 'invoice_form':form,'orderformset' : orderformset}
	if request.method == 'POST':
		user = request.user
		# print('user '+str(user.id))
		#print('printing POST:',request.POST)
		form = Create_invoice(request.POST)
		orderformset = orderitemFormset(request.POST)
		if form.is_valid():
			# print('user '+str(user.id))
			# form.save()
			customer_name = form.cleaned_data.get('customer_name')
			address =  form.cleaned_data.get('address')
			district = form.cleaned_data.get('district')
			invoice(customer_name=customer_name,address=address,district=district,user = user).save()
			# form_mapped.user=user
			# form_mapped.save()
			bill=invoice.objects.get(invoice_complete = False, user = user)
			# setrelation(bill.id)
			bill.bill_no='bixy'+str(bill.id)
			bill.save()
			bill= invoice.objects.get(invoice_complete = False, user = user)
			order=Order.objects.create()
			order.invoice_id=bill
			order.save()
			if orderformset.is_valid():
				# print('inside if2')
				for form in orderformset:
					if flag :
						flag = 0
						order_id = order
						# print(order)
						product = form.cleaned_data.get('product')
						dyn_product = medicine.objects.get(medicine_name = product)
						quantity = form.cleaned_data.get('quantity')
						if quantity <= dyn_product.medicine_stock_available:
							flag=1
							dyn_product.medicine_stock_available = dyn_product.medicine_stock_available - quantity
							dyn_product.save()
							price_billed = form.cleaned_data.get('price_billed')
							total_price_order = get_total_of_this_item(quantity,price_billed)
							bill_total = bill_total+total_price_order
							if order_id:
								#print(product)
								orderitem(order_id=order_id,product=product,quantity=quantity,price_billed=price_billed,total_price_order=total_price_order).save()
						else:
							return HttpResponse('<h1>billquantity exceed retry<h1>')
				order.order_total = bill_total
				order.save()
			return redirect( 'http://127.0.0.1:8000/invoice/htmlbill' )
	return render(request, 'invoice/forms.html', context)


def htmlbill(request):
	user = request.user
	bill = invoice.objects.get(invoice_complete = False, user = user)
	order = Order.objects.get(complete=False,invoice_id=bill)
	bill_total = order.order_total
	order.complete = True
	bill.invoice_complete = True
	order.save()
	bill.save()
	# order_item = []
	order_item = orderitem.objects.filter(order_id = order)
	context = {'order_item' : order_item, 'bill' : bill , 'bill_total':bill_total}
	return render(request, 'invoice/index.html',context)


def htmlbillsearch(request,pk):
	bill = invoice.objects.get(id = pk)
	order = Order.objects.get(invoice_id=bill)
	bill_total = order.order_total
	order_item = orderitem.objects.filter(order_id = order)
	context = {'order_item' : order_item, 'bill' : bill , 'bill_total':bill_total}
	return render(request, 'invoice/index.html',context)


def getpdf(request,pk):
	user = request.user
	invo = invoice.objects.get(id = pk)
	order = Order.objects.get(invoice_id = invo)
	order_item = orderitem.objects.filter(order_id = order)
	context = {'order_item' : order_item, 'bill' : invo}
	template = get_template('invoice/index.html')
	data_p = template.render(context)
	response = BytesIO()

	pdfpage = pisa.pisaDocument(BytesIO(data_p.encode('UTF-8')),response)
	if not pdfpage.err:
		return HttpResponse(response.getvalue(),content_type='application/pdf')
	else:
		return HttpResponse('error generating pdf')



def invoicesearch(request):

    invoice_obj = invoice.objects.all()
    #comp_obj = company.objects.all()
    myfilter = myFilter(request.GET,queryset = invoice_obj)
    invoice_obj= myfilter.qs
    context ={ 'invoice':invoice_obj , 'filter':myfilter  }
    return render(request, 'invoice/inv_search.html',context)
