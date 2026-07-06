from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import SignupAPIView, MeAPIView, LogoutAPIView



urlpatterns = [
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeAPIView.as_view(), name="me"),
    path("logout/", LogoutAPIView.as_view(), name="auth-logout"),
]