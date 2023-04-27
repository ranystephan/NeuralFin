from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Stock, Transaction
from .serializers import StockSerializer, TransactionSerializer

class StockListCreateView(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]

class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


import yfinance as yf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class StockInfoView(APIView):
    def get(self, request, symbol):
        try:
            stock_info = yf.Ticker(symbol).info
            return Response(stock_info)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
