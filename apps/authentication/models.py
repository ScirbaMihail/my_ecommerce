from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from apps.authentication.managers import CustomUserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    class Sex(models.TextChoices):
        female = 'F', 'Female'
        male = 'M', 'Male'

    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    birth_date = models.DateField(default=timezone.now)
    sex = models.CharField(choices=Sex.choices)

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def username(self):
        return self.email

    def __str__(self):
        return f'{self.email=} -> {self.birth_date=}, {self.sex=}'

    class Meta:
        db_table = 'users'
