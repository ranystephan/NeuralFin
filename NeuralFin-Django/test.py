from finvizfinance.quote import finvizfinance

stock = finvizfinance('AAPL')

stock_fundament = stock.ticker_fundament()






symbol='AAPL'
name=stock_fundament.get('Company')
index=stock_fundament.get('Index')
sector=stock_fundament.get('Sector')
industry=stock_fundament.get('Industry')

print(stock_fundament)
print(symbol)
print(name)
print(index)
print(sector)
print(industry)

