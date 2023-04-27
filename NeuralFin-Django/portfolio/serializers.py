from rest_framework import serializers
from .models import Stock, Portfolio, PortfolioStock

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class PortfolioStockSerializer(serializers.ModelSerializer):
    stock = StockSerializer()

    class Meta:
        model = PortfolioStock
        fields = ('stock', 'shares')

class PortfolioSerializer(serializers.ModelSerializer):
    stocks = PortfolioStockSerializer(many=True, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Portfolio
        fields = ('id', 'name', 'user', 'stocks')
