from django import forms
from .models import Cost


class CostForm(forms.ModelForm):
    class Meta:
        model = Cost
        fields = ('capital', 'others', 'special')
        labels = {
            'capital': 'شهرهای بزرگ',
            'others': 'سایر شهذها',
            'special': 'آگهی ویژه',
        }
