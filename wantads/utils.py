from utils.models import BaseModel
from django.db import models
from django.conf import settings

user = settings.AUTH_USER_MODEL


class WandADBase(BaseModel):
    want = models.ForeignKey('WantAd', on_delete=models.CASCADE,
                             related_name="%(app_label)s_%(class)s",
                             related_query_name="%(app_label)s_%(class)s",
                             )
    user = models.ForeignKey(user, on_delete=models.CASCADE,
                             related_name="%(app_label)s_%(class)s",
                             related_query_name="%(app_label)s_%(class)s",
                             )

    class Meta:
        abstract = True
