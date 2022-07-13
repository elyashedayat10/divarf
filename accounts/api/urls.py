from django.urls import path

from .views import SendOtpApiView, VerifyApiView, UserWantListApiView, UserWantRetrieveApiView

urlpatterns = [
    path("send_otp/", SendOtpApiView.as_view()),
    path("verify/", VerifyApiView.as_view()),
    path('my_wants/', UserWantListApiView.as_view()),
    path('my_want_detail/<int:id>/', UserWantRetrieveApiView.as_view())
]
