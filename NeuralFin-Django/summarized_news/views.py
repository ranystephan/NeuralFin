""" from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import SummarizedArticle


def index(request):

    return HttpResponse("Hello, world. You're at the summarized_news index.")
"""
from django.shortcuts import render
from django.http import HttpResponse
from .models import SummarizedArticle


from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt

from .news_summarizer import summarization_results


@csrf_exempt
@require_GET
def summarize_news(request):
    """
    Specs:
    Description: Returns a list of summarized news articles for the given ticker(s) to the client (to be dispalyed in the frontend).
    URL: /summarized_news/
    Uses: news_summarizer.summarization_results()
    """
    
    
    # ticker = request.GET.get('ticker')

    ###
    #testing with a sample ticker list
    ticker_list = ['AAPL']
    ###

    """ 
    if ticker:
        ticker_list = [ticker]
    else:
        ticker_list = request.GET.getlist('tickers[]', []) 
    """

    if not ticker_list:
        return JsonResponse({'error': 'Please provide at least one ticker.'}, status=400)

    results = summarization_results(ticker_list)

    ###
    context = {'results': results}
    #return render(request, 'summarized_news.html', context)
    ###

    return JsonResponse({'results': results})
