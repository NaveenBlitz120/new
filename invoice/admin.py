from django.contrib import admin
from stock.models import medicine
from .models import *
# Register your models here.


admin.site.register(invoice)
admin.site.register(Order)
admin.site.register(orderitem)
