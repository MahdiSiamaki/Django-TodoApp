from typing import Dict, Any

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "email", "is_verified"]


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, max_length=100, min_length=4)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password1"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if data["password"] != data["password1"]:
            raise serializers.ValidationError({"password": "Passwords must match."})

        try:
            validate_password(data["password"])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({"email": "Email is already in use."})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, data):
        if data["new_password"] != data["new_password1"]:
            raise serializers.ValidationError({"new_password": "Passwords must match."})

        try:
            validate_password(data["new_password"])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs, **kwargs) -> Dict[str, Any]:
        data = super().validate(attrs)
        data["username"] = self.user.username
        data["email"] = self.user.email
        data["is_verified"] = self.user.is_verified
        if not self.user.is_verified:
            msg = _("User account is disabled.")
            raise serializers.ValidationError(msg, code="authorization")
        return data


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        if not User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({"email": "Email does not exist."})
        return data
