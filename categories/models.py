from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(
        max_length=125,
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="children",
    )
    paid = models.BooleanField(default=False)

    class MPTTMeta:
        order_insertion_by = ("name",)

    def __str__(self):
        return self.name

    @property
    def children_count(self):
        return self.get_descendant_count()
