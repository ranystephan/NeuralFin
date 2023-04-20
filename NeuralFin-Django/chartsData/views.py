import yfinance as yf
from datetime import datetime
from rest_framework.views import APIView


def get_data_chart(symbol):
    ticker = yf.Ticker(symbol)
    
    data = ticker.history(period="2y")
    data = data.reset_index()
    data['date'] = data['Date'].apply(lambda x: datetime.strftime(x, '%Y-%m-%d'))
    data.drop(['Date'], axis=1, inplace=True)

    
    return data.to_dict('records')

from django.http import JsonResponse

class ChartAPIView(APIView):
    def get(self, request, symbol):
        chart_data = get_data_chart(symbol.upper())
        return JsonResponse({'chart_data': chart_data})