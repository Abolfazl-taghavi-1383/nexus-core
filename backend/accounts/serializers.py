from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

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

        
        
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)

    def validate(self, attrs):
        self.refresh = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.refresh)
            token.blacklist()
        except TokenError:
            raise serializers.ValidationError(
                {"refresh": "Invalid or expired refresh token."}
            )