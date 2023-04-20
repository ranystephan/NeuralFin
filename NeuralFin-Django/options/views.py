import yfinance as yf
from rest_framework.views import APIView
from dateutil.parser import parse
from django.http import JsonResponse




def get_data_option_exp(symbol):

    ticker = yf.Ticker(symbol)
  
    exp_dates = ticker.options
    
    exp_data = exp_dates
    


    return exp_data
  
  
def get_data_option_chains(symbol, exp_date):
  ticker = yf.Ticker(symbol)
  
  optionChains = ticker.option_chain(exp_date)
  
  chains_data = {}
  
  chains_data['calls'] = optionChains.calls.to_dict('records')
  chains_data['puts'] = optionChains.puts.to_dict('records')
  
  return chains_data  



class OptionsExpAPIView(APIView):
  def get(self, request, symbol):
      exp_data = get_data_option_exp(symbol.upper())
      return JsonResponse({'exp_data': exp_data})
    


class OptionsChainsAPIView(APIView):
    def get(self, request, symbol, exp_date):
        chains_data = get_data_option_chains(symbol.upper(), exp_date)
        return JsonResponse({'chains_data': chains_data})