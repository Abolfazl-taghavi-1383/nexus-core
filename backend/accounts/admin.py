from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Platform Profile", {"fields": ("phone_number", "avatar", "is_verified")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Platform Profile", {"fields": ("phone_number", "avatar", "is_verified")}),
    )
    list_display = (
        "username",
        "email",
        "phone_number",
        "is_verified",
        "is_staff",
        "is_active",
    )
    search_fields = (
        "username",
        "email",
        "phone_number",
        "first_name",
        "last_name",
    )
