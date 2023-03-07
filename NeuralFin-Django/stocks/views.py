from django.shortcuts import render

import requests
from django.http import JsonResponse

import os
import environ
env = environ.Env()
environ.Env.read_env()


def get_stock_data(request, symbol):
    api_key = env('ALPHA_VANTAGE_API_KEY')
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data)
