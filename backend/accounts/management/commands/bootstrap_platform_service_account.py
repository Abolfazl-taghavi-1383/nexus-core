import secrets

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


User = get_user_model()


class Command(BaseCommand):
    help = "Create or update the platform service account used for internal service-to-service access."

    def handle(self, *args, **options):
        username = "platform_service"
        email = "platform-service@example.local"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
                "is_verified": True,
                "is_service_account": True,
            },
        )

        updated = False

        if user.email != email:
            user.email = email
            updated = True

        if not user.is_active:
            user.is_active = True
            updated = True

        if user.is_staff:
            user.is_staff = False
            updated = True

        if user.is_superuser:
            user.is_superuser = False
            updated = True

        if not getattr(user, "is_verified", False):
            user.is_verified = True
            updated = True

        if not getattr(user, "is_service_account", False):
            user.is_service_account = True
            updated = True

        generated_password = None
        if created:
            generated_password = secrets.token_urlsafe(32)
            user.set_password(generated_password)
            updated = True

        if updated:
            user.save()

        if created:
            self.stdout.write(self.style.SUCCESS("Platform service account created successfully."))
            self.stdout.write(f"username: {username}")
            self.stdout.write(f"password: {generated_password}")
            self.stdout.write(self.style.WARNING("Store this password securely. It will not be shown again."))
        else:
            self.stdout.write(self.style.SUCCESS("Platform service account already exists and has been reconciled."))
