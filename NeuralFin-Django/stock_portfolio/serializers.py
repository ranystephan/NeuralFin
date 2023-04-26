from rest_framework import serializers
from .models import Stock, Portfolio


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ('id', 'symbol', 'company_name')

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ('id', 'user', 'stock', 'shares')
