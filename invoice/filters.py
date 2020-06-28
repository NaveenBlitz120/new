import django_filters
from .models import invoice
from django_filters import CharFilter,DateFilter
from django.contrib.auth.models import User

class myFilter(django_filters.FilterSet):
    bill_no=CharFilter(field_name='bill_no',lookup_expr='icontains')
    customer_name=CharFilter(field_name='customer_name',lookup_expr='icontains')
    date_created=DateFilter(field_name='date_created',lookup_expr='gte')
    class meta:
        model = invoice
        fields = ['customer_name','date_created','bill_no']
