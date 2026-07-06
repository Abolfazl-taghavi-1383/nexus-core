from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
    )
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
