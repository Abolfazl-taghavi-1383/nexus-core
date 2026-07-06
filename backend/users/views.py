from accounts.permissions import IsServiceAccountOrAdmin
from rest_framework.views import APIView, status, Response
from rest_framework import generics, permissions

from .serializers import UserPublicSerializer, UserBulkRequestSerializer, UserListSerializer, User



class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAdminUser]

class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserPublicSerializer
    permission_classes = [IsServiceAccountOrAdmin]
    lookup_field = "id"
    
    
class UserBulkAPIView(APIView):
    permission_classes = [IsServiceAccountOrAdmin]

    def post(self, request):
        serializer = UserBulkRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_ids = serializer.validated_data["ids"]

        users = User.objects.filter(
            id__in=user_ids,
            is_active=True,
        )

        response_serializer = UserPublicSerializer(
            users,
            many=True,
            context={"request": request},
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )