# Generated by Django 3.2.14 on 2022-07-11 12:26

import django.db.models.deletion
import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wantads", "0008_auto_20220711_1103"),
    ]

    operations = [
        migrations.CreateModel(
            name="IPAddress",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ip_address", models.GenericIPAddressField()),
            ],
        ),
        migrations.CreateModel(
            name="WantAdHit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", django_jalali.db.models.jDateField(auto_now_add=True)),
                (
                    "ip_address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wantads.ipaddress",
                    ),
                ),
                (
                    "want",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="wantads.wantad"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="wantad",
            name="hits",
            field=models.ManyToManyField(
                blank=True,
                related_name="hits",
                through="wantads.WantAdHit",
                to="wantads.IPAddress",
            ),
        ),
    ]
