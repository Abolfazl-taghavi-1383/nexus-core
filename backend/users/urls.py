from django.urls import path
from .views import UserListAPIView, UserBulkAPIView, UserRetrieveAPIView


urlpatterns = [
    path("", UserListAPIView.as_view(), name="user-list"),
    path("bulk/", UserBulkAPIView.as_view(), name="user-bulk"),
    path("<uuid:id>/", UserRetrieveAPIView.as_view(), name="user-detail"),
]
