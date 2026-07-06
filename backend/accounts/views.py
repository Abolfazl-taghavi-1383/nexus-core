from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SignupSerializer, UserMeSerializer, UserListSerializer, User, UserPublicSerializer, UserBulkRequestSerializer


class SignupAPIView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]


class MeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserMeSerializer(request.user, context={"request": request})
        return Response(serializer.data)


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAdminUser]
    
    
class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"
    
    
class UserBulkAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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