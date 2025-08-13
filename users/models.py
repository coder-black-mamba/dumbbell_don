from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

# internal imports
from .managers import CustomUserManager
from .validators import bd_phone_number_validator


class User(AbstractUser):
    MEMBER = 'MEMBER'
    STAFF = 'STAFF'
    ADMIN = 'ADMIN'
    ROLE_CHOICES = (
        (MEMBER, 'Member'),
        (STAFF, 'Staff'),
        (ADMIN, 'Admin')
    )
    username = None
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=MEMBER)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, validators=[bd_phone_number_validator])
    profile_picture = CloudinaryField('image', blank=True, null=True)
    address = models.TextField()    
    join_date = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    related_name = "user"
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'address']

    objects = CustomUserManager()


    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name} - {self.role}"
    
    @property
    def profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        return None
        
    