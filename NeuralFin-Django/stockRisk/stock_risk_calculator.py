import yfinance as yf
import numpy as np
import pandas as pd


# Getting the risk score for the average percentage change

def calculate_percentage_returns_score(stock_data, start_date='2018-01-01', end_date='2021-01-01'):
    """
    Determine the stock's historical returns: Look at the stock's historical prices and calculate the percentage change
    in price for each time period (day, week, month, etc.) to determine its historical returns.

    Args:
        tick (str): The stock ticker symbol.
        p (str, optional): The time period to look at. Defaults to "1y".
        i (str, optional): The interval to look at. Defaults to "1mo".

    Returns:
        pd.DataFrame: A dataframe containing the historical prices and percentage change in price for each time period.
        
    Raises:
        ValueError: If tick is not a valid stock ticker symbol.
    """
    listOfPercentageChange = [0]
    
    for i in range(1, len(stock_data)):
        avgMonth1 = (stock_data["Open"][i-1] + stock_data["Close"][i-1])/2
        avgMonth2 = (stock_data["Open"][i] + stock_data["Close"][i])/2
        
        listOfPercentageChange.append(((avgMonth2 - avgMonth1)/avgMonth1)*100)
    
    stock_data["Percentage Change"]  = listOfPercentageChange
    mean = np.mean(listOfPercentageChange)
    
    score = (1 / (1 + np.exp(-10 * (mean))))
    
    return score


# Getting the risk score for beta

def calculate_beta_score(stock_data, benchmark, start_date='2018-01-01', end_date='2021-01-01'):
    """It takes in a ticker and optionally a period and an interval and calculates the beta of the different indexes and funds it is present in

    Args:
        tick (str): The stock ticker symbol.
        start_date (str): At what date we want it to start
        end_date (str): At what date we want it to end
    
    Returns:
        Integer between 0 and 1 
    """
    # Calculate the daily returns of the stock
    stock_returns = stock_data['Adj Close'].pct_change()

    # Calculate the daily returns of the index
    benchmark_returns = benchmark['Adj Close'].pct_change()

    # Calculate the covariance and variance of the stock and the index
    covariance = stock_returns.cov(benchmark_returns)
    benchmark_variance = benchmark_returns.var()

    # Calculate the beta of the stock
    beta = covariance / benchmark_variance

    # Transform it into a value between 0 and 1 to get the score
    beta_score = 1 / (1 + np.exp(-4 * (beta - 1.25)))
    
    return beta_score


# Getting the risk score the standard deviation

def calculate_standard_deviation_score(stock_data, start_date='2018-01-01', end_date='2021-01-01'):
    """_summary_

    Args:
        stock_symbol (_type_): _description_
        start_date (str, optional): _description_. Defaults to '2018-01-01'.
        end_date (str, optional): _description_. Defaults to '2021-01-01'.

    Returns:
        _type_: _description_
    """
    # Calculate the daily returns of the stock
    stock_returns = stock_data['Adj Close'].pct_change()

    # Calculate the standard deviation of the returns
    standard_deviation = np.std(stock_returns)

    # The distribution was already very good and did not need  much transformation
    score = standard_deviation * 20
    
    return score


# Getting the risk score the volatility

def calculate_volatility_score(stock_data, start_date='2018-01-01', end_date='2021-01-01'):
    """_summary_

    Args:
        stock_symbol (_type_): _description_
        start_date (str, optional): _description_. Defaults to '2018-01-01'.
        end_date (str, optional): _description_. Defaults to '2021-01-01'.

    Returns:
        _type_: _description_
    """
    # Calculate the daily returns of the stock
    stock_returns = stock_data['Adj Close'].pct_change()

    # Calculate the volatility of the returns
    volatility = np.std(stock_returns) * np.sqrt(len(stock_returns))

    # The distribution was already very good and did not need  much transformation
    score = volatility - 0.2
    
    return score


# Getting the risk score the alpha

def calculate_alpha_score(stock_data, benchmark, start_date='2018-01-01', end_date='2021-01-01'):
    """
    Calculate the alpha of a stock using yfinance.

    Parameters:
        ticker (str): Ticker symbol of the stock.

    Returns:
        alpha (float): Alpha of the stock.
    """

    # Calculate the daily returns of the stock
    daily_returns = stock_data['Adj Close'].pct_change()

    # Get the daily returns of the market (SPY)
    market_returns = benchmark['Adj Close'].pct_change()

    # Calculate the CAPM beta of the stock
    beta = (daily_returns.cov(market_returns)) / (market_returns.var())

    # Calculate the expected return of the stock using CAPM
    rf = 0.01  # 1% risk-free rate
    market_return = market_returns.mean()
    expected_return = rf + beta * (market_return - rf)

    # Calculate the alpha of the stock
    stock_return = daily_returns.mean()
    alpha = stock_return - expected_return
    
    # Transform it into a value between 0 and 1 to get the score
    score = 1 / (1 + np.exp(-250 * (alpha)))

    return score


# Getting the risk score the Maximum Drawdown

def max_drawdown_score(stock_data, start_date, end_date):
    """
    Calculates the Maximum Drawdown for a stock between start_date and end_date.

    Parameters:
    - stock: string representing the stock symbol, e.g. "AAPL" for Apple Inc.
    - start_date: string representing the start date in the format "YYYY-MM-DD".
    - end_date: string representing the end date in the format "YYYY-MM-DD".

    Returns:
    - Float representing the Maximum Drawdown as a percentage.
    """

    # Calculate the cumulative maximum of the stock prices
    cum_max = stock_data['Adj Close'].cummax()

    # Calculate the drawdowns by dividing the stock prices by the cumulative maximum and subtracting 1
    drawdowns = (stock_data['Adj Close'] / cum_max) - 1

    # Calculate the Maximum Drawdown as the minimum of the drawdowns
    max_drawdown = drawdowns.min()
    
    # Transform it into a value between 0 and 1 to get the score
    score =  (((max_drawdown * -100) ** 0.5) - 3)/7
    return score


# Getting the risk score the Maximum Drawdown



# Calculating the risk score for a stock

def calculate_entire_score(ticker, start_date='2021-01-01', end_date='2023-01-01', benchmark_symbol='^GSPC'):
    """_summary_

    Args:
        ticker (_type_): _description_
        start_date (str, optional): _description_. Defaults to '2018-01-01'.
        end_date (str, optional): _description_. Defaults to '2021-01-01'.
        benchmark_symbol (str, optional): _description_. Defaults to '^GSPC'.
    """
    
    # Calculate all statistical metrics
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    benchmark = yf.download(benchmark_symbol, start=start_date, end=end_date)
    
    percentage_return_score = calculate_percentage_returns_score(stock_data, start_date, end_date)
    beta_score = calculate_beta_score(stock_data, benchmark,  start_date, end_date)
    std_score = calculate_standard_deviation_score(stock_data, start_date, end_date)
    volatility_score = calculate_volatility_score(stock_data, start_date, end_date)
    alpha_score = calculate_alpha_score(stock_data, benchmark, start_date, end_date)
    drawdown_score = max_drawdown_score(stock_data, start_date, end_date)
    
    print('pcr', percentage_return_score)
    print('beta', beta_score)
    print('std', std_score)
    print('volatility', volatility_score)
    print('alpha', alpha_score)
    print('Maximum drawdown', drawdown_score)
    
    
    # Add them up and adjust their values to get a score from 0 to 10
    
    score = percentage_return_score + beta_score + std_score + volatility_score + alpha_score + drawdown_score
    score = (score*10)/6
    
    return round(score, 2)

# Get the S&P 500 index from Wikipedia
# sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]

# tickers = sp500.Symbol.to_list()
# score_for_all = []

# for element in tickers:
#     score_for_all.append(calculate_entire_score(element))
# print(score_for_all)