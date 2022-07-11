from django.db import models
from django_jalali.db import models as jmodels


class BaseModel(models.Model):
    created = jmodels.jDateField(auto_now_add=True)
    updated = jmodels.jDateField(auto_now=True)

    class Meta:
        abstract = True
