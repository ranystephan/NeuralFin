import pandas as pd
from finvizfinance.quote import finvizfinance as ff



from rest_framework.views import APIView


def get_data_stock(symbol):
    stock = ff(symbol)
    stock_data = {}
    
    stock_data['fundamental'] = stock.ticker_fundament()
    

    return stock_data

from django.http import JsonResponse

class StockAPIView(APIView):
    def get(self, request, symbol):
        stock_data = get_data_stock(symbol.upper())
        return JsonResponse({'stock_data': stock_data})