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

@app.route('/')
def get_news():
    query = request.args.get('publication')
    if not query or query.lower() not in rss_feeds:
        publication = 'bbc'
    else:
        publication = query.lower()

    feed = feedparser.parse(rss_feeds[publication])

    weather = get_weather('London,UK')
    return render_template('home.html',
                           articles=feed['entries'],
                           weather=weather)


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
                   'city':parsed['name']}
    return weather


if __name__ == '__main__':
    app.run(port=5000, debug=True)
