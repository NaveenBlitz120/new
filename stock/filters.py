import django_filters
from .models import medicine
from django_filters import CharFilter

class myFilter(django_filters.FilterSet):
    medicinename=CharFilter(field_name='medicine_name',lookup_expr='contains')

    class meta:
        model = medicine
        fields = ['medicine_name']
