import requests

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction

from allauth.socialaccount.models import SocialAccount

User = get_user_model()


class SocialAuthError(Exception):
    pass


def _generate_unique_username(email: str) -> str:
    base_username = email.split("@")[0].strip().lower()
    base_username = "".join(
        char for char in base_username if char.isalnum() or char in ["_", "."]
    )

    if not base_username:
        base_username = "user"

    username = base_username
    counter = 1

    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    return username


def exchange_google_code_for_token(code: str) -> str:
    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_OAUTH_REDIRECT_URI,
            "grant_type": "authorization_code",
        },
        timeout=10,
    )

    if response.status_code != 200:
        raise SocialAuthError("Could not exchange Google authorization code.")

    data = response.json()
    access_token = data.get("access_token")

    if not access_token:
        raise SocialAuthError("Google access token was not returned.")

    return access_token


def fetch_google_profile(access_token: str) -> dict:
    response = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        timeout=10,
    )

    if response.status_code != 200:
        raise SocialAuthError("Could not fetch Google profile.")

    data = response.json()

    email = data.get("email")
    email_verified = data.get("email_verified")

    if not email:
        raise SocialAuthError("Google account does not have an email.")

    if not email_verified:
        raise SocialAuthError("Google email is not verified.")

    return {
        "provider": "google",
        "uid": str(data.get("sub")),
        "email": email.lower().strip(),
        "first_name": data.get("given_name", ""),
        "last_name": data.get("family_name", ""),
        "avatar": data.get("picture", ""),
        "extra_data": data,
    }


def exchange_github_code_for_token(code: str) -> str:
    response = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={
            "Accept": "application/json",
        },
        data={
            "code": code,
            "client_id": settings.GITHUB_OAUTH_CLIENT_ID,
            "client_secret": settings.GITHUB_OAUTH_CLIENT_SECRET,
            "redirect_uri": settings.GITHUB_OAUTH_REDIRECT_URI,
        },
        timeout=10,
    )

    if response.status_code != 200:
        raise SocialAuthError("Could not exchange GitHub authorization code.")

    data = response.json()

    if data.get("error"):
        raise SocialAuthError(data.get("error_description", "GitHub OAuth error."))

    access_token = data.get("access_token")

    if not access_token:
        raise SocialAuthError("GitHub access token was not returned.")

    return access_token


def fetch_github_profile(access_token: str) -> dict:
    user_response = requests.get(
        "https://api.github.com/user",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
        },
        timeout=10,
    )

    if user_response.status_code != 200:
        raise SocialAuthError("Could not fetch GitHub profile.")

    user_data = user_response.json()

    emails_response = requests.get(
        "https://api.github.com/user/emails",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
        },
        timeout=10,
    )

    if emails_response.status_code != 200:
        raise SocialAuthError("Could not fetch GitHub emails.")

    emails = emails_response.json()

    primary_verified_email = next(
        (
            item
            for item in emails
            if item.get("primary") is True and item.get("verified") is True
        ),
        None,
    )

    if not primary_verified_email:
        raise SocialAuthError("GitHub verified primary email is required.")

    full_name = user_data.get("name") or ""
    name_parts = full_name.split(" ", 1)

    first_name = name_parts[0] if len(name_parts) >= 1 else ""
    last_name = name_parts[1] if len(name_parts) == 2 else ""

    email = primary_verified_email["email"]

    return {
        "provider": "github",
        "uid": str(user_data.get("id")),
        "email": email.lower().strip(),
        "first_name": first_name,
        "last_name": last_name,
        "avatar": user_data.get("avatar_url", ""),
        "extra_data": {
            "github_user": user_data,
            "github_emails": emails,
        },
    }


@transaction.atomic
def get_or_create_user_from_social_profile(profile: dict):
    provider = profile["provider"]
    uid = profile["uid"]
    email = profile["email"]

    social_account = (
        SocialAccount.objects
        .select_related("user")
        .filter(provider=provider, uid=uid)
        .first()
    )

    if social_account:
        user = social_account.user

        if not user.is_active:
            raise SocialAuthError("This account is disabled.")

        return user, False, False

    user = User.objects.filter(email=email).first()
    user_created = False

    if user:
        if not user.is_active:
            raise SocialAuthError("This account is disabled.")
    else:
        user = User.objects.create_user(
            email=email,
            username=_generate_unique_username(email),
            password=None,
            first_name=profile.get("first_name", ""),
            last_name=profile.get("last_name", ""),
        )

        if hasattr(user, "avatar"):
            user.avatar = profile.get("avatar", "")

        if hasattr(user, "is_verified"):
            user.is_verified = True

        user.save()
        user_created = True

    SocialAccount.objects.create(
        user=user,
        provider=provider,
        uid=uid,
        extra_data=profile.get("extra_data", {}),
    )

    return user, user_created, True


def authenticate_with_google(code: str):
    access_token = exchange_google_code_for_token(code)
    profile = fetch_google_profile(access_token)

    return get_or_create_user_from_social_profile(profile)


def authenticate_with_github(code: str):
    access_token = exchange_github_code_for_token(code)
    profile = fetch_github_profile(access_token)

    return get_or_create_user_from_social_profile(profile)
