from random import randint

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.db.models import Count, F
from ..models import OtpCode
from ..utils import send_otp
from .serializers import PhoneSerializer, VerifySerializer

user = get_user_model()


class SendOtpApiView(GenericAPIView):
    serializer_class = PhoneSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.validated_data["phone_number"]
            random_number = randint(111111, 999999)
            otp_code = OtpCode.objects.create(
                phone_number=phone_number, code=random_number
            )
            send_otp(phone_number, random_number)
            contex = {
                "is_done": True,
                "message": "کد برای کاربر ارسال شد",
            }
            return Response(data=contex, status=status.HTTP_200_OK)
        context = {
            "is_done": False,
            "message": serializer.errors,
        }
        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)


class VerifyApiView(GenericAPIView):
    serializer_class = VerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number, code = (
                serializer.validated_data["phone_number"],
                serializer.validated_data["code"],
            )
            otp_obj = OtpCode.objects.filter(phone_number=phone_number)
            if otp_obj.code == str(code):
                try:
                    user_obj = user.objects.get(phone_number=phone_number)
                    token, create = Token.objects.get_or_create(user_id=user_obj.id)
                    context = {
                        "is_done": True,
                        "message": "کاربر با موفقیت وارد شد",
                        "data": token.key,
                    }
                    return Response(data=context, status=status.HTTP_200_OK)
                except:
                    user_obj = user.objects.create_user(phone_number=phone_number)
                    token = Token.objects.create(user=user_obj)
                    context = {
                        "is_done": True,
                        "message": "کاربر با موفقیت ساخته شد",
                        "data": token.key,
                    }
                    return Response(data=context, status=status.HTTP_200_OK)
            else:
                context = {
                    "is_done": False,
                    "message": "رمز وارد شده درست نمیباشذ",
                }
                return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
        else:
            context = {
                "is_done": False,
                "message": serializer.errors,
            }
            return Response(data=context, status=status.HTTP_502_BAD_GATEWAY)


#
# class LogoutApiView(GenericAPIView):

from wantads.api.serializers import WandAdSerializers
from wantads.models import WantAd


class UserWantListApiView(GenericAPIView):
    serializer_class = WandAdSerializers

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=request.user.want_ad.all(), many=True, context={'request': request})
        context = {
            'is_done': True,
            'message': ' لیست آگهی های کاربر',
            'data': serializer.data
        }
        return Response(data=context, status=status.HTTP_200_OK)


class UserWantRetrieveApiView(GenericAPIView):
    serializer_class = WandAdSerializers

    def get(self, request, *args, **kwargs):
        want_id = kwargs.get('id')
        queryset = WantAd.objects.filter(id=want_id).annotate(hits_count=F('hits__created1')).order_by('hits')
        serializer = self.serializer_class(instance=queryset, many=True, context={'request': request})
        context = {
            'is_done': True,
            'message': 'جزییات آگهی کاربر',
            'data': serializer.data
        }
        return Response(data=context, status=status.HTTP_200_OK)
