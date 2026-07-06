from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "password_confirm",
        )
        read_only_fields = ("id",)

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        if password != password_confirm:
            raise serializers.ValidationError(
                {"password_confirm": "Password confirmation does not match."}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")

        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user


class UserMeSerializer(serializers.ModelSerializer):
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
            "date_joined",
        )
        read_only_fields = fields


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
            "email",
            "phone_number",
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
    
    
    