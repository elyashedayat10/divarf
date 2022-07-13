from django.urls import path
from .views import (
    TicketListView,
    TicketDetailView,
)

app_name = 'ticket'

urlpatterns = [
    path('', TicketListView.as_view(), name="list"),
    path('<int:pk>/', TicketDetailView.as_view(), name='detail')
]
