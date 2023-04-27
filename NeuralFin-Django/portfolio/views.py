from rest_framework import viewsets, status
from .models import Stock, Portfolio
from .serializers import StockSerializer, PortfolioSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class PortfolioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_stock(self, request, pk=None):
        try:
            portfolio = self.get_queryset().get(pk=pk)
        except Portfolio.DoesNotExist:
            return Response({"error": "Portfolio not found"}, status=status.HTTP_404_NOT_FOUND)

        stock_symbol = request.data.get('symbol')
        shares = request.data.get('shares')
        if not stock_symbol or not shares:
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        stock, _ = Stock.objects.get_or_create(symbol=stock_symbol)
        stock.shares = shares
        stock.save()

        portfolio.stocks.add(stock)
        portfolio.save()

        return Response({"message": "Stock added to portfolio"})


    @action(detail=True, methods=['post'])
    def remove_stock(self, request, pk=None):
        try:
            portfolio = self.get_queryset().get(pk=pk)
        except Portfolio.DoesNotExist:
            return Response({"error": "Portfolio not found"}, status=status.HTTP_404_NOT_FOUND)

        stock_symbol = request.data.get('symbol')
        if not stock_symbol:
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            stock = portfolio.stocks.get(symbol=stock_symbol)
            portfolio.stocks.remove(stock)
            portfolio.save()
            return Response({"message": "Stock removed from portfolio"})
        except Stock.DoesNotExist:
            return Response({"error": "Stock not found in portfolio"}, status=status.HTTP_404_NOT_FOUND)

