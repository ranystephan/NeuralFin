from finvizfinance.quote import finvizfinance
import yfinance as yf

stock = finvizfinance('AAPL')

stockYF = yf.Ticker('AAPL')

market_price = stockYF.fast_info['lastPrice']

print(market_price)

#stock_fundament = stock.ticker_fundament()


#print(stock_fundament)


