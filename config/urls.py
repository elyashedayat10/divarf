from django.urls import path

from .views import PanelView, StaticView

app_name = "config"
urlpatterns = [
    path("", PanelView.as_view(), name="panel"),
    path(
        "static/",
        StaticView.as_view(),
        name="static",
    ),
]
