import datetime
from django.db import models
from users.models import User
from stocks.models import Stock
from django.utils import timezone

import yfinance as yf

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
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
    transaction_date = models.DateTimeField(default=timezone.now)


    transaction_type = models.CharField(
        max_length=4,
        choices=TransactionType.choices,
        default=TransactionType.BUY,
    )

    def get_stock_market_price_and_date(stock_symbol):
        stock = yf.Ticker(stock_symbol)
        market_data = stock.history(period='1m', interval='1m')
        
        first_valid_index = market_data.first_valid_index()
        
        market_price = stock.fast_info['lastPrice']
        market_date = first_valid_index
        
        return market_price, market_date

    def save(self, *args, **kwargs):
        self.stock_symbol = self.stock.symbol
        if self.purchase_price is None or self.transaction_date is None:
            market_price, market_date = PortfolioItem.get_stock_market_price_and_date(self.stock.symbol)
            if self.purchase_price is None:
                self.purchase_price = market_price
            if self.transaction_date is None:
                self.transaction_date = timezone.make_aware(datetime.datetime.fromtimestamp(market_date))
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.stock.symbol} - {self.shares} shares"
