from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("wantads.urls", namespace="want_ad")),
    path("category/", include("categories.urls")),
    path("panel/", include("config.urls", namespace="config")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("ticket/", include("tickets.urls", namespace="ticket")),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns = urlpatterns + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += [
        path("silk/", include("silk.urls", namespace="silk")),
        path("__debug__/", include("debug_toolbar.urls")),
    ]
