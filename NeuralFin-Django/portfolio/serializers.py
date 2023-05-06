from rest_framework import serializers
from .models import Portfolio, PortfolioItem

class PortfolioSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_email = serializers.EmailField(read_only=True)

    class Meta:
        model = Portfolio
        fields = ['id', 'user', 'user_email', 'name', 'description']

class PortfolioItemSerializer(serializers.ModelSerializer):
    stock_symbol = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = PortfolioItem
        fields = ['id', 'portfolio', 'stock', 'stock_symbol', 'shares', 'purchase_price', 'transaction_type']
