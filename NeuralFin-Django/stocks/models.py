from django.db import models



class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)  # Added unique=True
    name = models.CharField(max_length=100)  # Add the name field
    index = models.CharField(max_length=50, default='N/A')  # Add the exchange field
    sector = models.CharField(max_length=50, null=True, blank=True)  # Add the sector field (optional)
    industry = models.CharField(max_length=50, null=True, blank=True)  # Add the industry field (optional)
    country = models.CharField(max_length=10, default='USA')  # Add the currency field

    def __str__(self):
        return f"{self.symbol} - {self.name}"
