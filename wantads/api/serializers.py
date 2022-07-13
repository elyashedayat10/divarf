import base64

from django.core.files.base import ContentFile
from drf_extra_fields.fields import Base64ImageField
from gprof2dot import basestring
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from categories.api.serializers import CategorySerializer

from ..models import Bookmark, Image, Note, WantAd

import uuid
import base64
import imghdr

from django.utils.translation import ugettext_lazy as _
from django.core.files.base import ContentFile
from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    image = Base64ImageField()


class WandAdSerializers(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField("want_ad:detail", lookup_field="pk")
    categories = serializers.SerializerMethodField()
    # images = serializers.SerializerMethodField()
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = WantAd
        fields = (
            "url",
            "id",
            "user",
            "title",
            "description",
            "active_chat",
            "categories",
            "city",
            "zone",
            "confirmed",
            "lat",
            "long",
            "show_phone",
            "data",
            "special",
            "logo",
        )
        read_only_fields = ("id", "user", "logo")
        # depth = 1
        # depth=1  show all info for relational fields

        #

    def get_categories(self, obj):
        return CategorySerializer(obj.category).data

    # def get_images(self, obj):
    #     return ImageSerializer(obj.images.all(), many=True).data


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ("user", "text", "want")
        read_only_fields = ("user",)


from rest_framework.validators import ValidationError


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ("user", "want")
        read_only_fields = ("user",)

    # def create(self, validated_data):
    #     user = validated_data.get('user')
    #     want = validated_data.get('want')
    #     if Bookmark.objects.filter(user=user, want=want).exists():
    #         raise ValidationError('already exist')
    #     return super().create(validated_data)


from django.contrib.auth import get_user_model

user_ob = get_user_model()

from collections import OrderedDict
import re
def decode_base64(data, altchars=b'+/'):

    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data, altchars)




class WandAdCreateSerializers(serializers.ModelSerializer):
    # external_image = ImageSerializer(many=True)
    external_image=serializers.ListField()

    class Meta:
        model = WantAd
        fields = (
            "id", "title", "description", "active_chat", "category", "city", "zone", "lat", "long", "show_phone",
            "data",
            "external_image"
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        images = validated_data.pop('external_image')
        want_obj = WantAd.objects.create(
            user=self.context['request'].user, **validated_data
        )
        for image in images:
            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]
            pad = len(imgstr) % 4
            phone=imgstr + "=" * pad
            data = ContentFile(base64.b64decode(phone), name='temp.' + ext)
            Image.objects.create(want=want_obj, image=data)
        return want_obj
