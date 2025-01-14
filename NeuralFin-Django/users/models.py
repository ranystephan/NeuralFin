from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True, null=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    
    
    #important for analysis of user data
    #user_age = models.CharField(max_length=255)

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
