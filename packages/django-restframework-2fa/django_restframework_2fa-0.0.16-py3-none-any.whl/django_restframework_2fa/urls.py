
import os
from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView
from django_restframework_2fa.views import Login2FARequestOTPView

urlpatterns = [
    path('request-login-otp/', Login2FARequestOTPView.as_view()),
    # path('verify-login-otp/', VerifyOTPForLoginView.as_view()),
    # path('get-new-access-token/', TokenRefreshView.as_view()),
]