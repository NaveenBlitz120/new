from django.db import models
from stock.models import medicine,company
from django.contrib.auth.models import User
# Create your models here.
class invoice(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null = True)
    bill_no = models.CharField(max_length=10, null=True)
    customer_name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=100, null=True)
    date_created = models.DateField(auto_now_add=True)
    invoice_complete = models.BooleanField(default=False)
    # @property
    # def generate(self):
    #     bill = 'bixy' + str(self.id)
    #     self.bill_no = bill


class Order(models.Model):
    invoice_id = models.ForeignKey(invoice, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    order_total = models.DecimalField( max_digits=10, decimal_places=2, null=True)


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

class orderitem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(medicine, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    price_billed = models.IntegerField(default=0, null=True, blank=True)
    total_price_order = models.IntegerField(default=0, null=True, blank=True)
    @property
    def get_total(self):
        total = self.price_billed * self.quantity
        return total
