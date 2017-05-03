import json
import os
from urllib.request import urlopen
from urllib.parse import quote

import feedparser
from flask import Flask, render_template, request


app = Flask(__name__)

rss_feeds = {'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn':'http://rss.cnn.com/rss/edition.rss',
             'fox':'http://feeds.foxnews.com/foxnews/latest',
             'onion':'http://www.theonion.com/feeds/rss'}

defaults = {'publication':'bbc',
            'city':'London,UK',
            'currency_from':'GBP',
            'currency_to':'USD'}

@app.route('/')
def home():
    publication = request.args.get('publication')
    if not publication:
        publication = defaults['publication']
    articles = get_news(publication)

    city = request.args.get('city')
    if not city:
        city = defaults['city']
    weather = get_weather(city)

    currency_from = request.args.get('currency_from')
    if not currency_from:
        currency_from = defaults['currency_from']
    currency_to = request.args.get('currency_to')
    if not currency_to:
        currency_to = defaults['currency_to']
    rate, currencies = get_rates(currency_from, currency_to)

    return render_template('home.html',
                           articles=articles,
                           weather=weather,
                           currency_from = currency_from,
                           currency_to = currency_to,
                           rate = rate,
                           currencies=sorted(currencies))


def get_news(query):
    if not query or query.lower() not in rss_feeds:
        publication = defaults['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(rss_feeds[publication])
    return feed['entries']


def get_rates(frm, to):
    currency_url = 'https://openexchangerates.org//api/latest.json?app_id={0}'.format(os.environ.get('OPENEXCHANGERATES_API_KEY', None))
    all_currency = urlopen(currency_url).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return to_rate/frm_rate, parsed.keys()


def get_weather(query):
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&appid={1}'
    query = quote(query)
    url = api_url.format(query, os.environ.get('OPENWXMAP_API_KEY', None))
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {'description':parsed['weather'][0]['description'],
                   'temperature':parsed['main']['temp'],
                   'city':parsed['name'],
                   'country':parsed['sys']['country'],
                   'windspeed':parsed['wind']['speed'],
                   'winddeg':parsed['wind']['deg']}
    return weather


if __name__ == '__main__':
    app.run(port=5000, debug=True)
