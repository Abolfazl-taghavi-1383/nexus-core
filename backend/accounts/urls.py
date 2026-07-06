from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import SignupAPIView, MeAPIView, UserListAPIView, UserBulkAPIView, UserRetrieveAPIView


urlpatterns = [
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeAPIView.as_view(), name="me"),
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("users/bulk/", UserBulkAPIView.as_view(), name="user-bulk"),
    path("users/<uuid:id>/", UserRetrieveAPIView.as_view(), name="user-detail"),
]