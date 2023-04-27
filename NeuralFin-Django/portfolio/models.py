from django.db import models
from users.models import User

class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    shares = models.IntegerField()
    transaction_type = models.CharField(max_length=10, choices=[('buy', 'buy'), ('sell', 'sell')])
    created_at = models.DateTimeField(auto_now_add=True)
