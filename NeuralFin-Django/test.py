from finvizfinance.quote import finvizfinance
import yfinance as yf
from datetime import datetime

#stock = finvizfinance('AAPL')

#print(stock.ticker_fundament())

stockYF = yf.Ticker('ABBV')

market_price = stockYF.history(period='1m', interval='1m')

last_price = stockYF.fast_info['lastPrice']


market_data = stockYF.history(period='1m', interval='1m')

first_valid_index = market_data.first_valid_index()

#fast = stockYF.fast_info['previousClose']
print(market_price)
print(last_price)

print("AAAAAAAAAAAAAAAAA")

print(first_valid_index)

#print(market_price)

#end_date = datetime.now().strftime("%Y-%m-%d")

#print(end_date)
#Interval required 5 minutes
#data = yf.download(tickers='AAPL', start='2023-04-29', end='2023-05-07' , interval='1h')
#Print data
#print(data)


#stock_fundament = stock.ticker_fundament()


#print(stock_fundament)


