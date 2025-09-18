from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import CustomUserManager  # if you put manager in a separate file
class DivisionChoices(models.TextChoices):
    DHAKA = 'Dhaka', 'Dhaka'
    CHITTAGONG = 'Chattogram', 'Chattogram'
    KHULNA = 'khulna', 'Khulna'
    RAJSHAHI = 'Rajshahi', 'Rajshahi'
    BARISHAL = 'Barishal', 'Barishal'
    SYLHET = 'Sylhet', 'Sylhet'
    RANGPUR = 'Rangpur', 'Rangpur'
    MYMENSINGH = 'Mymensingh', 'Mymensingh'
class CustomUser(AbstractBaseUser, PermissionsMixin):
    token=models.PositiveIntegerField(null=True)
    is_varified=models.BooleanField(default=False)
    id=models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    address=models.TextField(null=True)
    division = models.CharField(
        max_length=20,
        choices=DivisionChoices.choices,
        default=DivisionChoices.DHAKA
    )
    phone_number=models.CharField(max_length=14,null=True)
    username = models.CharField(max_length=100, blank=True, null=False,unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email