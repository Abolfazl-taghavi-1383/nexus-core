from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SignupSerializer, UserMeSerializer, LogoutSerializer


class SignupAPIView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]


class MeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserMeSerializer(request.user, context={"request": request})
        return Response(serializer.data)


class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_205_RESET_CONTENT,
        )