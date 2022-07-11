from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, View, DetailView
from utils.mixins import AdminAccessMixin
from .filters import WantAdFilter
from .models import WantAd


# Create your views here.
def home(request):
    return render(request, "base.html")


class WantAdListView(ListView):
    template_name = 'wantads/list.html'
    context_object_name = 'filter'

    def get_queryset(self):
        f = WantAdFilter(request=self.request.GET, queryset=WantAd.objects.filter(confirmed=True))
        return f


class NotConfirmedWantAdView(AdminAccessMixin, ListView):
    queryset = WantAd.objects.filter(confirmed=False)
    template_name = "wantads/notconfirmed.html"


class WantAdDetailView(AdminAccessMixin, DetailView):
    model = WantAd
    template_name = 'wantads/detail.html'
    context_object_name = 'want_ad'


class ConfirmWantAdView(AdminAccessMixin, View):
    def get(self, request, *args, **kwargs):
        want_id = kwargs.get("pk")
        want_obj = get_object_or_404(WantAd, id=want_id)
        want_obj.confirmed = True
        want_obj.save()
        messages.success(request, "", "success")
        return redirect("want_ad:not_confirmed")
