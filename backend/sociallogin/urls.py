from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import GoogleSocialLoginAPIView, GitHubSocialLoginAPIView


urlpatterns = [
    path("google/", GoogleSocialLoginAPIView.as_view(), name="social-google-login"),
    path("github/", GitHubSocialLoginAPIView.as_view(), name="social-github-login"),
]