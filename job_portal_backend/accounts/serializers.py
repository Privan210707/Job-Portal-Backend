from rest_framework import serializers
from .models import User, UserRole

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'role',
        ]
    def validate_role(self, value):
        if value == UserRole.ADMIN:
            raise serializers.ValidationError(
                'Admin accounts cannot be created through registration.'
            )
        return value
    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user