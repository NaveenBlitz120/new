from django.forms import ModelForm
from .models import medicine


class Create(ModelForm):
	class Meta:
		model = medicine
		fields = '__all__'

class Update(ModelForm):
	class Meta:
		model = medicine
		fields = [ 'medicine_open_stock','medicine_stock_available', ]