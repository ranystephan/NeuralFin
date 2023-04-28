from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Portfolio
from .serializers import PortfolioSerializer
from users.models import User
from stocks.models import Stock
from stocks.serializers import StockSerializer
from stocks.utils import calculate_portfolio_value_and_pnl


class PortfolioView(APIView):
    def get(self, request):
        user = request.user
        portfolio = Portfolio.objects.filter(user=user).first()
        serializer = PortfolioSerializer(portfolio)
        
        portfolio_stocks = portfolio.stocks.all()
        total_value, total_pnl = calculate_portfolio_value_and_pnl(portfolio_stocks)
        response_data = {
            "portfolio": serializer.data,
            "total_value": total_value,
            "total_pnl": total_pnl
        }
        return Response(response_data)

        
        
    def post(self, request):
        user = request.user
        serializer = PortfolioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        portfolio = Portfolio.objects.filter(user=user).first()
        if not portfolio:
            return Response(status=status.HTTP_404_NOT_FOUND)
        stock_symbol = request.data.get('stock_symbol')
        action = request.data.get('action')
        if action == 'add':
            stock, _ = Stock.objects.get_or_create(symbol=stock_symbol)
            portfolio.stocks.add(stock)
        elif action == 'remove':
            stock = Stock.objects.filter(symbol=stock_symbol).first()
            if stock:
                portfolio.stocks.remove(stock)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = PortfolioSerializer(portfolio)
        return Response(serializer.data)
