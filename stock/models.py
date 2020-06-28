from django.db import models

# Create your models here.
class company(models.Model):
    company_name=models.CharField(max_length=100)
    contact_no=models.CharField(max_length=10,unique=True)
    mail=models.EmailField(max_length=254)

    def __str__(self):
        return self.company_name

class medicine(models.Model):

    category=[
    ('solid','solid'),
    ('liquid','liquid')
    ]
    weight=[
    ('kg','kg'),
    ('ltr','ltr'),
    ('tonnes','tonnes')
    ]
    medicine_name = models.CharField(max_length=100)
    company_name = models.ForeignKey(company,null=True,on_delete=models.SET_NULL)
    medicine_type = models.CharField(max_length=50,null=True,choices=category)
    medicine_open_stock = models.FloatField(null=True)
    medicine_stock_available = models.FloatField(null=True)
    medicine_stock_type = models.CharField(max_length=50,choices=weight,null=True)
    medicine_mrp = models.DecimalField( max_digits=5, decimal_places=2, null=True)

    def __str__(self):
        return str(self.medicine_name)
