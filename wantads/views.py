from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, View
from django.db.models import Q, Sum

from utils.mixins import AdminAccessMixin

from .filters import WantAdFilter, PayingFilter
from .models import WantAd


# Create your views here.
def home(request):
    return render(request, "base.html")


class WantAdListView(ListView):
    template_name = "wantads/list.html"
    context_object_name = "filter"

    def get_queryset(self):
        f = WantAdFilter(
            request=self.request.GET, queryset=WantAd.objects.filter(confirmed=True)
        )
        return f


class NotConfirmedWantAdView(AdminAccessMixin, ListView):
    queryset = WantAd.objects.filter(confirmed=False)
    template_name = "wantads/notconfirmed.html"


class WantAdDetailView(AdminAccessMixin, DetailView):
    model = WantAd
    template_name = "wantads/detail.html"
    context_object_name = "want_ad"


class ConfirmWantAdView(AdminAccessMixin, View):
    def get(self, request, *args, **kwargs):
        want_id = kwargs.get("pk")
        want_obj = get_object_or_404(WantAd, id=want_id)
        want_obj.confirmed = True
        want_obj.save()
        messages.success(request, "", "success")
        return redirect("want_ad:not_confirmed")


class PaidWantView(AdminAccessMixin, ListView):
    queryset = WantAd.objects.filter(special=True)
    template_name = 'wantads/paid.html'
    context_object_name = 'special_list'

    def get_context_data(self, *args, **kwargs):
        context_data = super(PaidWantView, self).get_context_data(*args, **kwargs)
        context_data['paid_count'] = self.get_queryset().count()
        return context_data


class SpecialWantView(AdminAccessMixin, ListView):
    queryset = WantAd.objects.filter(special=True)
    template_name = 'wantads/special.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(SpecialWantView, self).get_context_data(*args, **kwargs)
        context_data['special_count'] = self.get_queryset().count()
        return context_data


class PayingListView(ListView):
    template_name = 'wantads/paying.html'
    context_object_name = 'filter'

    def get_queryset(self):
        f = PayingFilter(
            request=self.request.GET, queryset=WantAd.objects.filter(special=True)
        )
        return f

    def get_context_data(self, *args, **kwargs):
        context_data = super(PayingListView, self).get_context_data(*args, **kwargs)
        # context_data['count'] = self.get_queryset().count()
        # context_data['total'] = WantAd.objects.filter(
        # id_in=self.get_queryset().values_list('id', flat=True)).aggregate()
        return context_data


































