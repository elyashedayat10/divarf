from django.urls import path

from .views import PanelView, StaticView, CostView,CostSetView

app_name = "config"
urlpatterns = [
    path("", PanelView.as_view(), name="panel"),
    path(
        "static/",
        StaticView.as_view(),
        name="static",
    ),
    path('cost/', CostView.as_view(), name="cost"),
    path('cost_set/',CostSetView.as_view(),name='cost_set')
]
