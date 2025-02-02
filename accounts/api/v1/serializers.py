from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_verified']

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, max_length=100, min_length=4)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password1']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password1']:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        
        try:
            validate_password(data['password'])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email is already in use.'})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['new_password1']:
            raise serializers.ValidationError({'new_password': 'Passwords must match.'})

        try:
            validate_password(data['new_password'])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        return data

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_verified:
            return {'user': user}
        msg = _('User account is disabled.')
        raise serializers.ValidationError(msg, code='authorization')
