from django.shortcuts import render

from rest_framework.views import APIView
from .serializers import  StockSerializer, PortfolioSerializer
from .models import Portfolio
from rest_framework.response import Response
from rest_framework import status


class PortfolioView(APIView):
    def get(self, request):
        user = request.user
        portfolio = user.portfolio
        serializer = PortfolioSerializer(portfolio)
        return Response(serializer.data)

    def post(self, request):
        serializer = PortfolioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)

    def delete(self, request, stock_id):
        user = request.user
        portfolio_item = Portfolio.objects.get(user=user, stock_id=stock_id)
        portfolio_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
