from django.shortcuts import render
from .filters import TicketFilter
from .models import Ticket
from django.views.generic import ListView, DetailView
# Create your views here.
from utils.mixins import AdminAccessMixin


class TicketListView(AdminAccessMixin, ListView):
    template_name = 'tickets/list.html'
    context_object_name = 'filter'

    def get_queryset(self):
        queryset = TicketFilter(request=self.request.GET, queryset=Ticket.objects.all())
        print(Ticket.objects.all())
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super(TicketListView, self).get_context_data(*args, **kwargs)
        context_data['count'] = self.get_queryset().queryset.count()
        return context_data


class TicketDetailView(AdminAccessMixin, DetailView):
    model = Ticket
    template_name = 'tickets/detail.html'
