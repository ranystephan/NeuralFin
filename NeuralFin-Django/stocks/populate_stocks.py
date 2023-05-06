from finvizfinance.quote import finvizfinance
import os
import django

import sys
from pathlib import Path

# Get the project root path
project_root = str(Path(__file__).resolve().parent.parent)
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NeuralFin_Django.settings')
django.setup()

from stocks.models import Stock

# List of stock symbols you want to fetch
stock_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'NIO', 'ABBV']

for symbol in stock_symbols:
    stock = finvizfinance(symbol)

    stock_fundament = stock.ticker_fundament()
    # Create a new stock instance
    stock_info = Stock(
        symbol=symbol,
        name=stock_fundament.get('Company'),
        index=stock_fundament.get('Index'),
        sector=stock_fundament.get('Sector'),
        industry=stock_fundament.get('Industry'),
        country=stock_fundament.get('Country'),
    )

    # Save the stock instance to the database
    stock_info.save()

    print(f"Saved stock: {stock_info.symbol} - {stock_info.name}")
