import yfinance as yf


def fetch_stock_data(ticker, start_date, end_date):
  stock = yf.Ticker(ticker)
  stock_data = stock.history(start=start_date, end=end_date)
  return stock_data
  
  
def calculate_portfolio_value_and_pnl(portfolio_stocks):
  total_value = 0
  total_pnl = 0
  
  for stock in portfolio_stocks:
    ticker = stock.ticker
    shares = stock.shares
    purchase_price = stock.purchase_price
    
    #fetch stock data 1d
    stock_data = fetch_stock_data(ticker, '1d')
    current_price = stock_data['Close'].iloc[-1]
    
    stock_value = shares * current_price
    stock_pnl = (current_price - purchase_price) * shares
    
    total_value += stock_value
    total_pnl += stock_pnl
    
    return total_value, total_pnl
    