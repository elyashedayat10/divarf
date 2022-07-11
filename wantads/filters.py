import django_filters
from .models import WantAd


class WantAdFilter(django_filters.FilterSet):
    class Meta:
        model = WantAd
        fields = (
            'category',
            'city',
        )
