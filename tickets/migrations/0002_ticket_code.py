# Generated by Django 3.2.14 on 2022-07-13 13:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='code',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]