from django.contrib import admin

from .models import Bookmark, Image, Viewed, WantAd


# Register your models here.
@admin.register(WantAd)
class WantAdAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "created",
    )


admin.site.register(Viewed)
admin.site.register(Bookmark)
admin.site.register(Image)
