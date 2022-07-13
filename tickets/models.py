import uuid

from django.db import models
from utils.models import BaseModel
from django.conf import settings
from django_jalali.db import models as jmodels

user = settings.AUTH_USER_MODEL
import random
import random


def create_new_ref_number():
    return str(random.randint(1000000000, 9999999999))


# Create your models here.
class Ticket(BaseModel):
    class TYPE(models.TextChoices):
        Technical =  'فنی' ,"1" # Technical
        financial =  'مالی',"2"  # Financial
        support =  'پشتیبانی',"3"  # Support

    class Status(models.TextChoices):
        waiting =  'در انتظار پاسخ','1'  # Waiting
        answered =  'پاسخ داده شده','2'  # Answeres
        closed =  'بسته شده','3'  # Closed

    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='tickets')
    text = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE.choices)
    status = models.CharField(max_length=20, choices=Status.choices)
    closed_at = jmodels.jDateField()
    code = models.CharField(max_length=124, unique=True, default=create_new_ref_number)


class Answer(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    WHO_CHOICES = [
        ('ادمین', 'ادمین'),  # َََAdmin
        ('کاربر', 'کاربر'),  # User
    ]
    from_who = models.CharField(max_length=20, choices=WHO_CHOICES)

    body = models.TextField()
