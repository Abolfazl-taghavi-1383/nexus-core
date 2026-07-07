from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    LoginAPIView,
    LogoutAPIView,
    MeAPIView,
    PasswordChangeAPIView,
    PasswordForgotAPIView,
    PasswordResetAPIView,
    RegisterAPIView,
)

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="auth-register"),
    path("login/", LoginAPIView.as_view(), name="auth-login"),

    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),

    path("logout/", LogoutAPIView.as_view(), name="auth-logout"),

    path("me/", MeAPIView.as_view(), name="auth-me"),

    path("password/change/", PasswordChangeAPIView.as_view(), name="password-change"),
    path("password/forgot/", PasswordForgotAPIView.as_view(), name="password-forgot"),
    path("password/reset/", PasswordResetAPIView.as_view(), name="password-reset"),
]