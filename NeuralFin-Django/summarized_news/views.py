""" from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import SummarizedArticle


def index(request):

    return HttpResponse("Hello, world. You're at the summarized_news index.")
 """
 
from django.shortcuts import render
from .news_summarizer import *

def process_data(request):
    if request.method == 'POST':
        input_tickers = request.POST.get('input_tickers')
        input_file_name = request.POST.get('input_file_name')

        # Process the data using functions from your script file
        raw_urls = {ticker:search_for_stock_news_urls(ticker) for ticker in input_tickers}
        cleaned_urls = {ticker:strip_unwanted_urls(raw_urls[ticker], excluded_list) for ticker in input_tickers}
        articles = {ticker:scrape_and_process(cleaned_urls[ticker]) for ticker in input_tickers} 
        summaries = {ticker:summarize(articles[ticker]) for ticker in input_tickers}
        scores = {ticker: sentiment(summaries[ticker]) for ticker in input_tickers}
        final_output = create_output_array(summaries, scores, cleaned_urls)
        final_output.insert(0, ['Ticker', 'Summary', 'Label', 'Confidence', 'URL' ])

        """         
        # Write the output to a CSV file
        with open(f'{input_file_name}', mode = 'w', newline = '') as f:
            csv_writer = csv.writer(f, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            csv_writer.writerows(final_output) 
        """

        # Render the output to a template
        context = {'output': final_output}
        return render(request, 'my_template.html', context)

    else:
        return render(request, 'my_form.html')
