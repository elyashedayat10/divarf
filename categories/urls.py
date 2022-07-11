from django.urls import include, path

from categories.api.urls import urlpatterns

from .views import (
    CategoryCreateView,
    CategoryDeleteVIew,
    CategoryDetailView,
    CategoryUpdateView,
    ParentCategoryListView,
)

app_name = "category"
urlpatterns = [
    path("", ParentCategoryListView.as_view(), name="parent"),
    path("<int:pk>/", CategoryDetailView.as_view(), name="detail"),
    path("create/", CategoryCreateView.as_view(), name="create"),
    path("update/<int:pk>/", CategoryUpdateView.as_view(), name="update"),
    path("delete/<int:pk>", CategoryDeleteVIew.as_view(), name="delete"),
    path("api/", include(urlpatterns)),
]
