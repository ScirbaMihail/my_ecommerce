from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.core.validators import MinValueValidator

from apps.authentication.managers import CustomUserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)], default=0
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def username(self):
        return self.email

    def __str__(self):
        return f"{self.email=} -> {self.balance=}"

    class Meta:
        db_table = "users"
