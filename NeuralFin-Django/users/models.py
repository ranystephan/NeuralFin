from django.db import models
from django.contrib.auth.models import AbstractUser
from stock_portfolio.models import Portfolio

#test
# Create your models here.
class User(AbstractUser):
    
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, null=True, related_name='user_portfolio')
    
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
