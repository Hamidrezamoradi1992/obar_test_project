from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import models



# Create your models here.


class CustomUserManager(UserManager):
    def _create_user(self, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        password = extra_fields.pop("password")
        user = self.model(**extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(**extra_fields)

    def create_superuser(self, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(**extra_fields)


class User(AbstractUser):
    username = None
    password = models.CharField(max_length=128, blank=True, null=True, unique=False)
    email = models.EmailField(unique=True, null=False,
                              validators=[EmailValidator])
    phone = models.CharField(max_length=11,
                             null=True,
                             blank=True,
                             unique=True)


    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    def __str__(self):
        return f'{self.email}-{self.get_full_name()}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [models.Index(fields=['email', 'first_name'])]
