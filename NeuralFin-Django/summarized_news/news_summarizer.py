import re  # regular expressions
import csv
from transformers import pipeline
from transformers import PegasusTokenizer, PegasusForConditionalGeneration, TFPegasusForConditionalGeneration
from bs4 import BeautifulSoup
import requests

model_name = "human-centered-summarization/financial-summarization-pegasus"
tokenizer = PegasusTokenizer.from_pretrained(
    model_name)  # what incodes and decodes our text
model = PegasusForConditionalGeneration.from_pretrained(
    model_name, resume_download=True)  # model itsef
    
def search_for_stock_news_urls(ticker):
    """  
    Specs:
    Requires: ticker
    Modifies: None
    Returns: list of urls
    Description: This function takes a ticker and returns a list of urls from google news
    """

    search_url = "https://www.google.com/search?q=yahoo+finance+{}&tbm=nws".format(
        ticker)
    r = requests.get(search_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # atags are the links in the google page (from yahoo in this case)
    atags = soup.find_all('a')
    hrefs = [link['href'] for link in atags]
    return hrefs


def strip_unwanted_urls(urls, exclude_list):
    """
    Specs:
    Requires: list of urls, list of words to exclude
    Modifies: None
    Returns: list of urls
    Description: This function takes a list of urls and a list of words to exclude and returns a list of urls that do not contain the words to exclude
    """

    val = []
    for url in urls:
        if 'https://' in url and not any(exclude_word in url for exclude_word in exclude_list):
            res = re.findall(r'(https?://\S+)', url)[0].split('&')[0]
            val.append(res)
    return list(set(val))


def scrape_and_process(URLs):
    """
    Specs:
    Requires: list of urls
    Modifies: None
    Returns: list of articles
    Description: This function takes a list of urls and returns a list of articles
    """

    ARTICLES = []
    for url in URLs:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = [paragraph.text for paragraph in paragraphs]
        words = ' '.join(text).split(' ')[:350]
        ARTICLE = ' '.join(words)
        ARTICLES.append(ARTICLE)
    return ARTICLES


def summarize(articles):
    """
    Specs:
    Requires: list of articles
    Modifies: None
    Returns: list of summaries
    Description: This function takes a list of articles and returns a list of summaries
    """
    summaries = []
    for article in articles:
        input_ids = tokenizer.encode(article, return_tensors='pt')
        output = model.generate(input_ids, max_length=55,
                                num_beams=5, early_stopping=True)
        summary = tokenizer.decode(output[0], skip_special_tokens=True)
        summaries.append(summary)
    return summaries


def create_output_array(ticker_list, summaries, scores, urls):
    """
    Specs:
    Requires: dictionary of summaries, dictionary of scores, dictionary of urls
    Modifies: None
    Returns: list of lists
    Description: This function takes a dictionary of summaries, a dictionary of scores, and a dictionary of urls and returns a list of lists
    """
    output = []
    for ticker in ticker_list:
        for counter in range(len(summaries[ticker])):
            output_this = [
                ticker,
                summaries[ticker][counter],
                scores[ticker][counter]['label'],
                scores[ticker][counter]['score'],
                urls[ticker][counter]
            ]
            output.append(output_this)
    return output


def summarization_results(ticker_list):
    """
    Specs:
    Requires: list of tickers
    Modifies: None
    Returns: list of lists
    Testing strategy: check that the length of the output is equal to the length of the ticker list, check that the first element of the output is a list of strings
    Description: This function takes a list of tickers and returns the results of the summarization pipeline
    """


    raw_urls = {ticker: search_for_stock_news_urls(
        ticker) for ticker in ticker_list} # dictionary of lists

    excluded_list = ['maps', 'policies', 'preferences', 'accounts', 'support']

    print("Cleaning urls...")
    cleaned_urls = {ticker: strip_unwanted_urls(
        raw_urls[ticker], excluded_list) for ticker in ticker_list}

    print("Scraping and processing articles...")
    articles = {ticker: scrape_and_process(
        cleaned_urls[ticker]) for ticker in ticker_list}

    print("Summarizing articles using Pegasus...")
    summaries = {ticker: summarize(articles[ticker]) for ticker in ticker_list}

    # Adding Sentiment Analysis Pipeline
    sentiment = pipeline('sentiment-analysis')

    print("Analyzing sentiment of summaries...")
    scores = {ticker: sentiment(summaries[ticker]) for ticker in ticker_list}

    print("Creating output array...")
    final_output = create_output_array(
        ticker_list, summaries, scores, cleaned_urls)

    final_output.insert(0, ['Ticker', 'Summary', 'Label', 'Confidence', 'URL'])

    return final_output
