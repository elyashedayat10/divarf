from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django_jalali.db import models as jmodels

from categories.models import Category
from utils.models import BaseModel

from .utils import WantAdBase

user = settings.AUTH_USER_MODEL


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField()


class WantAd(BaseModel):
    # class STATUS(models.TextChoices):
    #     accepted = "1", "تایید شده"
    #     rejected = "2", "تایید نشده"
    #     awaiting_payment = "3", "در انتظار پرداخت"

    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name="want_ad")
    title = models.CharField(max_length=125)
    description = models.TextField()
    active_chat = models.BooleanField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="want_ad"
    )
    city = models.CharField(max_length=125)
    zone = models.CharField(max_length=125)
    confirmed = models.BooleanField()
    lat = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    long = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    show_phone = models.BooleanField()
    data = models.JSONField()
    # cost = models.PositiveIntegerField(null=True, blank=True)
    special = models.BooleanField(default=True)
    hits = models.ManyToManyField(
        IPAddress,
        through="WantAdHit",
        blank=True,
        related_name="hits",
    )
    # status = models.CharField(max_length=15, choices=STATUS)

    objects = jmodels.jManager()

    class Meta:
        ordering = (
            "special",
            "created",
        )

    def __str__(self):
        return f"{self.user} اگهی {self.title} را در تاریخ {self.created} ثبت کرده "

    def get_absolute_url(self):
        return reverse("want_ad:detail", args=[self.pk])

    @property
    def logo(self):
        try:
            want_logo = self.images.first()
            return want_logo.image.url
        except:
            return None

    def hits_count(self):
        return self.hits.count()


class Image(BaseModel):
    want = models.ForeignKey(WantAd, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="")

    def clean(self):
        if self.want.images.count() > 20:
            raise ValidationError("حذاکثر عکس برای هر ۀگهی 20 عدد است")


class Note(WantAdBase):
    text = models.TextField()


class Bookmark(WantAdBase):
    pass


class Viewed(WantAdBase):
    pass


class WantAdHit(models.Model):
    want = models.ForeignKey(WantAd, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = jmodels.jDateField(auto_now_add=True)
    created1 = models.DateField()
