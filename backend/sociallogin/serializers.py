from rest_framework import serializers


class SocialLoginSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Authorization code is required.")

        return value