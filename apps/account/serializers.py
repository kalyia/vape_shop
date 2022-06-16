from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser

User = get_user_model()  # внутри лежит AUTH_USER_MODEL


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():  # проверили имейл на соответствие базе данных перед сохранением
            raise serializers.ValidationError('Email already exists')
        return email

    def validate(self, attrs: dict):
        pass1 = attrs.get('password')
        pass2 = attrs.pop('password_confirm')  # удаляем поле чтобы оно не пошло в базу данных т.к. оно нам там не нужно
        if pass1 != pass2:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def save(self):
        data = self.validated_data  # сюда падает validate_email и validate
        user = User.objects.create_user(**data)
        user.set_activation_code()
        user.send_activation_email()


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6)

    def validate_email(self, email):
        if not User.objects.filter(
                email=email).exists():  # проверили имейл на соответствие базе данных перед сохранением
            raise serializers.ValidationError("Email doesn't exists")
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.pop('password')
        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid password')
        if user and user.is_active:
            refresh = self.get_token(user)
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
        return attrs
