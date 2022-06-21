from django.contrib.auth.models import UserManager, AbstractBaseUser
from django.db import models
from django.core.mail import send_mail
from django.db.models.signals import post_save

from .services.signals import post_create_cart_signal


class CustomUserManager(UserManager):
    def _create(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Email cannot be empty')
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_staff', False)
        return self._create(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields['is_active'] = True

        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=8, blank=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username", ]

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj):
        return self.is_staff

    @staticmethod  # для генерации активэйшн кода
    def generate_activation_code():
        from django.utils.crypto import get_random_string
        code = get_random_string(8)
        return code

    def set_activation_code(self):  # создает активационный код и восстановление пароля
        code = self.generate_activation_code()
        if CustomUser.objects.filter(activation_code=code).exists():
            self.set_activation_code()
        else:
            self.activation_code = code
            self.save()

    def send_activation_email(self):
        activation_url = f'http://localhost:8000/account/activate/{self.activation_code}'
        message = f'You are signed up sucessfuly! Activate your account {activation_url}'
        send_mail("activate your account", message, 'test@gmail.com', [self.email, ], fail_silently=False)


post_save.connect(post_create_cart_signal, CustomUser)