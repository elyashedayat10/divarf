from django.shortcuts import get_object_or_404
from rest_framework import generics, response, status
from rest_framework.response import Response

from ..models import Category
from .serializers import CategorySerializer


class CategoryApiView(generics.GenericAPIView):
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        # try:
        # category_list = Category.objects.filter(parent=None)
        category_list = Category.objects.filter(parent=None)
        serializer = self.serializer_class(category_list, many=True)
        context = {
            "is_done": True,
            "message": "لیست دسته بندی ها",
            "data": serializer.data,
        }
        return Response(data=context)

    # except:
    #     context = {
    #         'is_done': False,
    #         'message': 'خطا دز انجام عملیات'
    #     }
    #     return Response(data=context)


#
# class CategoryWantApiView(generics.GenericAPIView):
#     serializer_class =
#
#     def get(self, request, *args, **kwargs):
#         try:
#             category_id = kwargs.get('id')
#             category_obj = get_object_or_404(Category, id=category_id)
#
