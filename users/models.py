from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# from cloudinary_storage.fields import CloudinaryField
from cloudinary.models import CloudinaryField
from .managers import CustomUserManager
# Create your models here.

bd_phone_number_validator = RegexValidator(
    regex=r'^\+8801\d{9}$',
    message="Phone number must be entered in the format: +8801234567890. Up to 15 digits allowed.",
)   

class User(AbstractUser):
    ROLE_CHOICES = (
        ('MEMBER', 'Member'),
        ('STAFF', 'Staff'),
        ('ADMIN', 'Admin')
    )
    username = None
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='MEMBER')
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, validators=[bd_phone_number_validator])
    profile_picture = CloudinaryField('image')
    address = models.TextField()    
    join_date = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    related_name = "user"
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'address']

    objects = CustomUserManager()
    