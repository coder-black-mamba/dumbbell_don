from django.db import models
from django.contrib.auth.models import AbstractUser
# from cloudinary_storage.fields import CloudinaryField
from cloudinary.models import CloudinaryField
# Create your models here.



class User(AbstractUser):
    ROLE_CHOICES = (
        ('MEMBER', 'Member'),
        ('STAFF', 'Staff'),
        ('ADMIN', 'Admin')
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='MEMBER')
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    profile_picture = CloudinaryField('image')
    address = models.TextField()    
    join_date = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    related_name = "user"
    