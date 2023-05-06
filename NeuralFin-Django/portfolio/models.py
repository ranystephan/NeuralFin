from django.db import models
from users.models import User
from stocks.models import Stock

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_email = models.EmailField()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.user_email = self.user.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class TransactionType(models.TextChoices):
    BUY = "buy", "Buy"
    SELL = "sell", "Sell"

class PortfolioItem(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=10)
    shares = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)


    transaction_type = models.CharField(
        max_length=4,
        choices=TransactionType.choices,
        default=TransactionType.BUY,
    )

    def save(self, *args, **kwargs):
        self.stock_symbol = self.stock.symbol
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.stock.symbol} - {self.shares} shares"
