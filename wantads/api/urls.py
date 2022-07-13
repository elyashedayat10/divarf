from django.urls import path

from .views import (
    BookmarkApiView,
    CategoryWantAdApiView,
    HomeApiView,
    NoteApiView,
    ViewedApiView,
    WantAdRetrieveAPIView,
    WantCreateApiView,
    ImageUploadApiView,
)

app_name = "want_ad"
urlpatterns = [
    path("home/", HomeApiView.as_view(), name="home"),
    path("<int:pk>/", WantAdRetrieveAPIView.as_view(), name="detail_api"),
    path("want_category/<int:id>/", CategoryWantAdApiView.as_view(), name="category"),
    path("recent_seen/", ViewedApiView.as_view(), name="seen"),
    path("bookmark/", BookmarkApiView.as_view(), name="bookmark"),
    path("note/", NoteApiView.as_view(), name="note"),
    path("create/", WantCreateApiView.as_view(), name="create"),
    path('image_upload/', ImageUploadApiView.as_view())
]
