import django_filters
from django import forms

from .models import WantAd


class WantAdFilter(django_filters.FilterSet):
    class Meta:
        model = WantAd
        fields = (
            "category",
            "city",
        )


class PayingFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='created', lookup_expr='year', label='سال')
    month = django_filters.NumberFilter(field_name='created', lookup_expr='month',
                                        label='ماه')
    day = django_filters.NumberFilter(field_name='created', lookup_expr='روز',
                                      label='Year Joined Less Than')
    # using jquery
    djfdate_time = django_filters.DateFilter(
        lookup_expr='icontains',
        widget=forms.DateInput(
            attrs={
                'id': 'datepicker',
                'type': 'text'
            }
        )
    )

    # name=django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'})
    # row_date = django_filters.DateFilter(
    #     widget=DateInput(
    #         attrs={
    #             'class': 'datepicker'
    #         }
    #     )
    # )
