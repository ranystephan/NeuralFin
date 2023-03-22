import yfinance as yf
from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_data_stock(request, symbol):
    # Retrieve historical stock price data
    stock = yf.Ticker(symbol)
    data = stock.history(period="max")
    # Convert the data to a dictionary
    data_dict = data.reset_index().rename(columns={'index': 'Date'}).to_dict('list')
    # Convert Timestamp values to string format
    data_dict['Date'] = [date.strftime('%Y-%m-%d') for date in data_dict['Date']]
    # Return the data as JSON
    return JsonResponse(data_dict)
