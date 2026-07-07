from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import AuthUserSerializer
from .serializers import SocialLoginSerializer
from .social_auth_service import (
    SocialAuthError,
    authenticate_with_github,
    authenticate_with_google,
)
from accounts.tokens import build_auth_tokens_for_user


class GoogleSocialLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SocialLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user, user_created, social_account_linked = authenticate_with_google(
                serializer.validated_data["code"]
            )
        except SocialAuthError as exc:
            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        tokens = build_auth_tokens_for_user(user)

        return Response(
            {
                "tokens": tokens,
                "user": AuthUserSerializer(user).data,
                "created": user_created,
                "social_account_linked": social_account_linked,
                "provider": "google",
            },
            status=status.HTTP_200_OK,
        )


class GitHubSocialLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SocialLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user, user_created, social_account_linked = authenticate_with_github(
                serializer.validated_data["code"]
            )
        except SocialAuthError as exc:
            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        tokens = build_auth_tokens_for_user(user)

        return Response(
            {
                "tokens": tokens,
                "user": AuthUserSerializer(user).data,
                "created": user_created,
                "social_account_linked": social_account_linked,
                "provider": "github",
            },
            status=status.HTTP_200_OK,
        )
        
        
class GoogleSocialCallbackTestAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        code = request.query_params.get("code")

        if not code:
            return Response(
                {"detail": "Authorization code is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user, user_created, social_account_linked = authenticate_with_google(code)
        except SocialAuthError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "tokens": build_auth_tokens_for_user(user),
                "user": AuthUserSerializer(user).data,
                "created": user_created,
                "social_account_linked": social_account_linked,
                "provider": "google",
            },
            status=status.HTTP_200_OK,
        )


class GitHubSocialCallbackTestAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        code = request.query_params.get("code")
        return Response({"code": code})