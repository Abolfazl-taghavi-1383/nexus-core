from rest_framework_simplejwt.tokens import RefreshToken


def build_auth_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    refresh["email"] = user.email
    refresh["username"] = user.username
    refresh["is_staff"] = user.is_staff
    refresh["is_service_account"] = getattr(user, "is_service_account", False)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }