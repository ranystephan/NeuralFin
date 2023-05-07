from finvizfinance.quote import finvizfinance
import yfinance as yf
from datetime import datetime

stock = finvizfinance('AAPL')

stockYF = yf.Ticker('AAPL')

market_price = stockYF.fast_info['lastPrice']

#print(market_price)

end_date = datetime.now().strftime("%Y-%m-%d")

print(end_date)
#Interval required 5 minutes
data = yf.download(tickers='AAPL', start='2023-04-29', end='2023-05-07' , interval='1h')
#Print data
print(data)


#stock_fundament = stock.ticker_fundament()


#print(stock_fundament)


