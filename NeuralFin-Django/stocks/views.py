import yfinance as yf
from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response


def get_data_stock(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1y")
    data = data.reset_index()
    data['date'] = data['Date'].apply(lambda x: datetime.strftime(x, '%Y-%m-%d'))
    data.drop(['Date'], axis=1, inplace=True)
    return data.to_dict('records')

from django.http import JsonResponse

class StockAPIView(APIView):
    def get(self, request, symbol):
        stock_data = get_data_stock(symbol.upper())
        return JsonResponse({'stock_data': stock_data})
