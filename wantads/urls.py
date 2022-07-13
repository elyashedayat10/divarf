from django.urls import include, path

from wantads.api.urls import urlpatterns

from .views import NotConfirmedWantAdView, WantAdDetailView, WantAdListView, home, SpecialWantView, PaidWantView, \
    PayingListView

app_name = "want_ad"
urlpatterns = [
    path("", home),
    path("not_confirmed/", NotConfirmedWantAdView.as_view(), name="not_confirmed"),
    path("list/", WantAdListView.as_view(), name="list"),
    path("paid/", PaidWantView.as_view(), name="paid"),
    path("special/", SpecialWantView.as_view(), name="special"),
    path("<int:pk>/", WantAdDetailView.as_view(), name="detail"),
    path('paying/', PayingListView.as_view(), name='paying'),
    path("api/", include(urlpatterns)),
]
