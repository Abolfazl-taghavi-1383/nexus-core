from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "avatar",
            "is_verified",
            "is_active",
            "is_staff",
            "date_joined",
        )
        read_only_fields = fields


class UserPublicSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "display_name",
            "avatar",
            "is_active",
            "is_verified",
        )
        read_only_fields = fields

    def get_display_name(self, obj):
        full_name = obj.get_full_name()
        return full_name if full_name else obj.username
    
    
class UserBulkRequestSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=False,
        max_length=1000,
    )
    
    
    