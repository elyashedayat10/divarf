from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from categories.api.serializers import CategorySerializer
from categories.models import Category

from ..models import Bookmark, Image, Note, Viewed, WantAd
from .serializers import (
    BookmarkSerializer,
    NoteSerializer,
    WandAdCreateSerializers,
    WandAdSerializers,
)

user = get_user_model()

from rest_framework.renderers import JSONRenderer
from rest_framework.utils import json


class JSONResponseRenderer(JSONRenderer):
    # media_type = 'text/plain'
    # media_type = 'application/json'
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_dict = {
            "status": "failure",
            "data": data,
            "message": "",
        }
        data = response_dict
        return json.dumps(data)


class HomeApiView(generics.GenericAPIView):
    queryset = WantAd.objects.all()
    serializer_class = WandAdSerializers
    renderer_classes = [JSONResponseRenderer]
    # def get(self, request, *args, **kwargs):
    # try:
    # serializer = WandAdSerializers(
    #     instance=queryset, many=True, context={"request": request}
    # )
    # context = {
    #     "is_done": True,
    #     "message": "لیست تمام محصولان",
    #     "data": serializer.data,
    # }
    # return Response(data=context, status=status.HTTP_200_OK)

    #     # except:
    #
    #     contex = {
    #     'is_done': False,
    #     'message': 'خطا در انجام عملیات'
    #     }
    # return Response(data=contex, status=status.HTTP_400_BAD_REQUEST)


class CategoryWantAdApiView(generics.GenericAPIView):
    serializer_class = WandAdSerializers

    def get(self, request, *args, **kwargs):
        category_id = kwargs.get("id")
        category_obj = get_object_or_404(Category, id=category_id)
        if category_obj.get_descendant_count() >= 1:
            category_list = category_obj.get_descendants(include_self=False)
            cat_serializer = CategorySerializer(instance=category_list, many=True).data
            want_list = WantAd.objects.filter(category__in=category_list)
            serializer = self.serializer_class(
                instance=want_list, many=True, context={"request": request}
            ).data
            context = {
                "is_done": True,
                "message": "لیست تمام محصولان",
                "data": {
                    "want_list": serializer,
                    "cat": cat_serializer,
                    "father_Cat": category_obj.name,
                },
            }
            return Response(data=context, status=status.HTTP_200_OK)
        else:
            want_list = category_obj.want_ad.all()
            serializer = self.serializer_class(
                want_list, many=True, context={"request": request}
            )
            context = {
                "is_done": True,
                "message": "لیست تمام محصولان  دسته بندی",
                "data": serializer.data,
            }
            return Response(data=context, status=status.HTTP_200_OK)


class WantAdRetrieveAPIView(generics.GenericAPIView):
    serializer_class = WandAdSerializers

    def get(self, request, *args, **kwargs):
        want_id = kwargs.get("pk")
        # try:
        queryset = get_object_or_404(WantAd, id=want_id)
        serializer = self.serializer_class(
            instance=queryset, context={"request": request}
        )
        viewed, get = Viewed.objects.get_or_create(user=request.user, want=queryset)
        bookmarked = Bookmark.objects.filter(want=queryset, user=request.user).exists()
        context = {
            "is_done": True,
            "message": "اطلاعات آگهی",
            "data": serializer.data,
            "bookmarked": bookmarked,
        }
        return Response(data=context, status=status.HTTP_200_OK)
        # except:
        #     context = {
        #         'is_done': False,
        #         'message': 'خطا دز انجام عملیات',
        #     }
        #     return Response(data=context, status=status.HTTP_200_OK)


class BookmarkApiView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        bookmark_list = request.user.wantads_bookmark.all()
        want_list = WantAd.objects.filter(id__in=bookmark_list)
        serializer = WandAdSerializers(
            instance=want_list, many=True, context={"request": request}
        )
        context = {
            "is_done": True,
            "message": "bookmark های کاربر",
            "data": serializer.data,
        }
        return Response(data=context, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = BookmarkSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            context = {
                "is_done": True,
                "message": "با موفقیت به bookmark ها اضافه شد",
                "data": serializer.data,
            }
            return Response(data=context, status=status.HTTP_200_OK)
        context = {
            "is_done": False,
            "message": "خطا در انجام عملیات",
            "data": serializer.errors,
        }
        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)


class NoteApiView(generics.GenericAPIView):
    serializer_class = NoteSerializer

    def get(self, request, *args, **kwargs):
        queryset = request.user.wantads_note.all()
        serializer = self.serializer_class(instance=queryset, many=True)
        context = {
            "is_done": True,
            "message": "یادداشت های کاربر",
            "data": serializer.data,
        }
        return Response(data=context, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        note = Note.objects.filter(user=request.user.id, want=serializer["want"])
        if note.exists():
            serializer = self.serializer_class(
                data=request.data, instance=note, partial=True
            )
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            context = {
                "is_done": True,
                "message": "عملیات با موفقیت انجام شد",
                "data": serializer.data,
            }
            return Response(data=context, status=status.HTTP_200_OK)
        context = {
            "is_done": True,
            "message": "خطا دز انجام عملیات",
            "data": serializer.errors,
        }
        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)


class ViewedApiView(generics.GenericAPIView):
    serializer_class = WandAdSerializers

    def get(self, request, *args, **kwargs):
        viewed_list = request.user.wantads_viewed.all().values_list("want", flat=True)
        want_list = WantAd.objects.filter(id__in=viewed_list)
        serializer = self.serializer_class(
            instance=want_list, many=True, context={"request": request}
        ).data
        context = {
            "is_done": True,
            "message": "لیست آگهی های اخیرا بازدید شده ",
            "data": serializer,
        }
        return Response(data=context, status=status.HTTP_200_OK)


from rest_framework.permissions import AllowAny

from .serializers import ImageSerializer


class WantCreateApiView(generics.GenericAPIView):
    serializer_class = WandAdCreateSerializers

    # permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        global want_id
        serializer = WandAdCreateSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            want_id = serializer.save(user=request.user, confirmed=True)
            # image_serializer = ImageSerializer(data=request.FILES, many=True)
            # if serializer.is_valid(raise_exception=True):
            #     image_serializer.save(want=want_id)
            context = {
                "is_done": True,
                "message": "با موفقیا ساخته شد ",
                "data": serializer.data,
            }
            return Response(data=context, status=status.HTTP_201_CREATED)
        context = {
            "is_done": False,
            "message": "خطا ",
            "data": serializer.errorse,
        }
        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
