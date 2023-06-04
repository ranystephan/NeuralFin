from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import Portfolio, PortfolioItem
from .serializers import PortfolioSerializer, PortfolioItemSerializer




class PortfolioListCreateView(generics.ListCreateAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

    def perform_create(self, serializer):
        token = self.request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            jwt_authentication = JWTAuthentication()
            validated_token = jwt_authentication.get_validated_token(token)
            user = jwt_authentication.get_user(validated_token)
        except InvalidToken:
            raise AuthenticationFailed('Unauthenticated!')

        serializer.save(user=user)

class PortfolioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer


    def get_queryset(self):
        token = self.request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            jwt_authentication = JWTAuthentication()
            validated_token = jwt_authentication.get_validated_token(token)
            user = jwt_authentication.get_user(validated_token)
        except InvalidToken:
            raise AuthenticationFailed('Unauthenticated!')

        return self.queryset.filter(user=user)

class PortfolioItemListCreateView(generics.ListCreateAPIView):
    serializer_class = PortfolioItemSerializer

    def get_queryset(self):
        token = self.request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            jwt_authentication = JWTAuthentication()
            validated_token = jwt_authentication.get_validated_token(token)
            user = jwt_authentication.get_user(validated_token)
        except InvalidToken:
            raise AuthenticationFailed('Unauthenticated!')

        return PortfolioItem.objects.filter(portfolio__user=user)

    def perform_create(self, serializer):
        token = self.request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            jwt_authentication = JWTAuthentication()
            validated_token = jwt_authentication.get_validated_token(token)
            user = jwt_authentication.get_user(validated_token)
        except InvalidToken:
            raise AuthenticationFailed('Unauthenticated!')


        portfolio = Portfolio.objects.get(user=user)
        serializer.save(portfolio=portfolio)

class PortfolioItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PortfolioItem.objects.all()
    serializer_class = PortfolioItemSerializer


    def get_queryset(self):
        token = self.request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            jwt_authentication = JWTAuthentication()
            validated_token = jwt_authentication.get_validated_token(token)
            user = jwt_authentication.get_user(validated_token)
        except InvalidToken:
            raise AuthenticationFailed('Unauthenticated!')

        return self.queryset.filter(portfolio__user=user)




import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


from rest_framework.views import APIView
from rest_framework.response import Response



class PortfolioMetricsView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            jwt_authentication = JWTAuthentication()
            validated_token = jwt_authentication.get_validated_token(token)
            user = jwt_authentication.get_user(validated_token)
        except InvalidToken:
            raise AuthenticationFailed('Unauthenticated!')
        
        portfolio_items = PortfolioItem.objects.filter(portfolio__user=user)
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")

        # Fetch historical stock data
        stock_data = {}
        for item in portfolio_items:
            stock = item.stock
            stock_info = yf.download(stock.symbol, start=start_date, end=end_date)
            stock_data[stock.symbol] = stock_info

        # Calculate metrics
        portfolio_value = self.calculate_portfolio_value(portfolio_items, stock_data)
        portfolio_returns = self.calculate_portfolio_returns(portfolio_items, stock_data)
        benchmark_data = yf.download("^GSPC", start=start_date, end=end_date)
        benchmark_returns = benchmark_data["Close"].pct_change().dropna()


        
        metrics = {
            "portfolio_value": portfolio_value,
            "portfolio_value_at_purchase": self.calculate_portfolio_value_at_purchase(portfolio_items),
            "pnl": self.calculate_pnl(portfolio_items, stock_data),
            "portfolio_performance": self.calculate_portfolio_performance(portfolio_items, stock_data),
            "beta": self.calculate_beta(portfolio_items, stock_data, start_date, end_date),
            "diversification": self.calculate_diversification(portfolio_items, stock_data),
            "value_at_risk": self.calculate_value_at_risk(portfolio_items, stock_data),
            "expected_shortfall": self.calculate_expected_shortfall(portfolio_items, stock_data),
            "sector_allocation": self.calculate_sector_allocation(portfolio_items),
            "sharpe_ratio": self.calculate_sharpe_ratio(portfolio_items, stock_data),
            "sortino_ratio": self.calculate_sortino_ratio(portfolio_items, stock_data),
            "information_ratio": self.calculate_information_ratio(portfolio_returns, benchmark_returns),
            "alpha": self.calculate_alpha(portfolio_returns, benchmark_returns),
            "information_coefficient": self.calculate_information_coefficient(portfolio_returns, benchmark_returns),
            "jensen_alpha": self.calculate_jensen_alpha(portfolio_returns, benchmark_returns),
        }

        return Response(metrics)

    def calculate_pnl(self, portfolio_items, stock_data):
        pnl = 0
        for item in portfolio_items:
            stock = yf.Ticker(item.stock.symbol)
            current_price = stock.fast_info['lastPrice']
            profit = (current_price - stock.fast_info['previousClose']) * item.shares
            pnl += profit
        return pnl
    
    def calculate_portfolio_performance(self, portfolio_items, stock_data):
        portfolio_value = self.calculate_portfolio_value(portfolio_items, stock_data)
        portfolio_value_at_purchase = self.calculate_portfolio_value_at_purchase(portfolio_items)
        percentagePerf = (portfolio_value - portfolio_value_at_purchase) / portfolio_value_at_purchase
        valuePerf = portfolio_value - portfolio_value_at_purchase
        
        return percentagePerf, valuePerf

    def calculate_beta(self, portfolio_items, stock_data, start_date, end_date):
        market_index_symbol = "^GSPC"  # S&P 500
        market_index_data = yf.download(market_index_symbol, start=start_date, end=end_date)
        market_returns = market_index_data["Close"].pct_change().dropna()

        portfolio_beta = 0
        for item in portfolio_items:
            stock = item.stock
            stock_returns = stock_data[stock.symbol]["Close"].pct_change().dropna()
            covariance = stock_returns.cov(market_returns)
            market_variance = market_returns.var()
            beta = covariance / market_variance

            # Calculate the weight of the stock in the portfolio
            stock_weight = (item.shares * float(item.purchase_price)) / self.calculate_portfolio_value(portfolio_items, stock_data)

            # Calculate the weighted beta
            weighted_beta = stock_weight * beta
            portfolio_beta += weighted_beta

        return portfolio_beta

    def calculate_portfolio_value(self, portfolio_items, stock_data):
        portfolio_value = 0
        
        for item in portfolio_items:
            stock = yf.Ticker(item.stock.symbol)
            current_price = stock.fast_info['lastPrice']
            value = current_price * item.shares
            portfolio_value += value
        return portfolio_value

    def calculate_portfolio_value_at_purchase(self, portfolio_items):
        portfolio_value_at_purchase = 0
        for item in portfolio_items:
            value_at_purchase = item.shares * float(item.purchase_price)
            portfolio_value_at_purchase += value_at_purchase
        return portfolio_value_at_purchase


    def calculate_portfolio_returns(self, portfolio_items, stock_data):
        weighted_returns = []
        
        for item in portfolio_items:
            stock = item.stock
            stock_returns = stock_data[stock.symbol]['Close'].pct_change().dropna()
            weight = (item.shares * float(item.purchase_price)) / self.calculate_portfolio_value(portfolio_items, stock_data)
            weighted_returns.append(stock_returns * weight)

        portfolio_returns = pd.concat(weighted_returns, axis=1).sum(axis=1)
        
        return portfolio_returns
    
    def calculate_diversification(self, portfolio_items, stock_data):
        stock_returns = []
        symbols = []

        for item in portfolio_items:
            stock = item.stock
            symbols.append(stock.symbol)
            stock_returns.append(stock_data[stock.symbol]['Close'].pct_change().dropna())

        returns_matrix = pd.concat(stock_returns, axis=1)
        returns_matrix.columns = symbols

        correlation_matrix = returns_matrix.corr()
        
        return correlation_matrix

    def calculate_value_at_risk(self, portfolio_items, stock_data, confidence_level=0.95):
        portfolio_returns = self.calculate_portfolio_returns(portfolio_items, stock_data)
        value_at_risk = -np.percentile(portfolio_returns, 100 * (1 - confidence_level))
        
        return value_at_risk

    def calculate_expected_shortfall(self, portfolio_items, stock_data, confidence_level=0.95):
        portfolio_returns = self.calculate_portfolio_returns(portfolio_items, stock_data)
        value_at_risk = self.calculate_value_at_risk(portfolio_items, stock_data, confidence_level)
        expected_shortfall = -np.mean(portfolio_returns[portfolio_returns < -value_at_risk])
        
        return expected_shortfall

    def calculate_sector_allocation(self, portfolio_items):
        sector_allocation = {}
        
        for item in portfolio_items:
            stock = item.stock
            sector = stock.sector
            value = item.shares * float(item.purchase_price)
            
            if sector in sector_allocation:
                sector_allocation[sector] += value
            else:
                sector_allocation[sector] = value

        total_value = sum(sector_allocation.values())
        sector_allocation = {k: v / total_value for k, v in sector_allocation.items()}
        
        return sector_allocation
    
    def calculate_sharpe_ratio(self, portfolio_items, stock_data):
        tnx = yf.Ticker("^TNX")
        risk_free_rate = tnx.fast_info['lastPrice'] / 100
        portfolio_returns = self.calculate_portfolio_returns(portfolio_items, stock_data)
        sharpe_ratio = (portfolio_returns.mean() - risk_free_rate) / portfolio_returns.std()
        
        return sharpe_ratio
    
    def calculate_sortino_ratio(self, portfolio_items, stock_data):
        tnx = yf.Ticker("^TNX")
        risk_free_rate = tnx.fast_info['lastPrice'] / 100
        portfolio_returns = self.calculate_portfolio_returns(portfolio_items, stock_data)
        sortino_ratio = (portfolio_returns.mean() - risk_free_rate) / portfolio_returns[portfolio_returns < 0].std()
        
        return sortino_ratio
    
    def calculate_information_ratio(self, portfolio_returns, benchmark_returns):
        information_ratio = (portfolio_returns - benchmark_returns).mean() / (portfolio_returns - benchmark_returns).std()
        
        return information_ratio
    
    def calculate_alpha(self, portfolio_returns, benchmark_returns):
        alpha = portfolio_returns.mean() - benchmark_returns.mean()
        
        return alpha
    
    def calculate_information_coefficient(self, portfolio_returns, benchmark_returns):
        information_coefficient = np.corrcoef(portfolio_returns, benchmark_returns)[0][1]
        
        return information_coefficient
    
    def calculate_jensen_alpha(self, portfolio_returns, benchmark_returns):
        beta, alpha = np.polyfit(benchmark_returns, portfolio_returns, deg=1)
        jensen_alpha = alpha - beta * benchmark_returns.mean()
        
        return jensen_alpha
    
    



from django.utils import timezone


class PortfolioValueOverTimeView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            jwt_authentication = JWTAuthentication()
            validated_token = jwt_authentication.get_validated_token(token)
            user = jwt_authentication.get_user(validated_token)
        except InvalidToken:
            raise AuthenticationFailed('Unauthenticated!')


        portfolio_items = PortfolioItem.objects.filter(portfolio__user=user)

        # Determine the date of the first transaction and set the start_date 7 days earlier
        first_transaction_date = portfolio_items.order_by("transaction_date").first().transaction_date.date()
        start_date = (first_transaction_date - timedelta(days=7)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")


        # Fetch historical stock data with an hourly interval
        stock_data = {}
        for item in portfolio_items:
            stock = item.stock
            stock_info = yf.download(stock.symbol, start=start_date, end=end_date, interval="1h")
            stock_info = stock_info.fillna(method='ffill')  # Fill missing values with the most recent available price
            stock_data[stock.symbol] = stock_info
        
        print("stock_data")
        print(stock_data)
        # Calculate the portfolio value over time
        portfolio_value_over_time = self.calculate_portfolio_value_over_time(portfolio_items, stock_data, start_date, end_date)

        return Response(portfolio_value_over_time)


    def calculate_portfolio_value_over_time(self, portfolio_items, stock_data, start_date, end_date):
        date_range = pd.date_range(start=start_date, end=end_date, freq="H")
        portfolio_value_over_time = {}

        last_close_values = {stock_symbol: 0 for stock_symbol in stock_data}

        for date in date_range:
            date = timezone.make_aware(date)
            portfolio_value = 0
            for stock_symbol, stock_info in stock_data.items():
                relevant_items = portfolio_items.filter(stock__symbol=stock_symbol, transaction_date__lte=date)
                if not stock_info.empty:
                    try:
                        current_price = stock_info.loc[stock_info.index <= date, "Close"].iloc[-1]
                        last_close_values[stock_symbol] = current_price
                    except IndexError:
                        current_price = last_close_values[stock_symbol]

                    for item in relevant_items:
                        value = current_price * item.shares
                        portfolio_value += value

            portfolio_value_over_time[date.strftime("%Y-%m-%d %H:%M:%S")] = portfolio_value

        return portfolio_value_over_time





