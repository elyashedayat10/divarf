from django.urls import include, path

from wantads.api.urls import urlpatterns

from .views import NotConfirmedWantAdView, home, WantAdDetailView,WantAdListView

app_name = "want_ad"
urlpatterns = [
    path("", home),
    path("not_confirmed/", NotConfirmedWantAdView.as_view(), name="not_confirmed"),
    path('list/',WantAdListView.as_view(),name='list'),
    path('<int:pk>/', WantAdDetailView.as_view(), name='detail'),
    path("api/", include(urlpatterns)),
]
