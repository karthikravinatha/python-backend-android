from abc import ABC

from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from .models import UserModel
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email_id', 'entity_id', 'first_name', 'last_name', 'mobile_number', 'is_super_user', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserModel.objects.create(**validated_data)
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)
        user = UserModel.objects.get(email_id=email)
        # encryptedpassword = make_password(password)
        check_pass = check_password(password, user.password)
        # user = authenticate(user_id=username, password=password) #This is not Working
        if not check_pass:
            raise serializers.ValidationError(
                'User with given name and password does not exists'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError(
                'User with given name and password does not exists'
            )
        return {
            "email": email,
            "token": jwt_token
        }
