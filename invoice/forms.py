from django.forms import ModelForm
from .models import *
from django.forms import formset_factory


class Create_invoice(ModelForm):
	class Meta:
		model = invoice
		fields = '__all__'
		exclude = ['id','bill_no','user','invoice_complete']

class create_orderitem(ModelForm):
	class Meta:
		model = orderitem
		fields = '__all__'
		exclude = ['order_id','total_price_order']
orderitemFormset = formset_factory(create_orderitem, extra=1)
