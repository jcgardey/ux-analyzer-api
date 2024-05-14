from rest_framework import serializers
from .models import User

class LoginUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

class SignUpUserSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField()

    class Meta:
        model = User
        fields = ('name', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }