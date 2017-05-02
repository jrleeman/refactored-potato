import feedparser
from flask import Flask, render_template

app = Flask(__name__)

rss_feeds = {'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn':'http://rss.cnn.com/rss/edition.rss',
             'fox':'http://feeds.foxnews.com/foxnews/latest',
             'onion':'http://www.theonion.com/feeds/rss'}

@app.route('/')
@app.route('/<source>')
def get_news(source='bbc'):
    feed = feedparser.parse(rss_feeds[source])
    return render_template('home.html',
                           articles=feed['entries'])

if __name__ == '__main__':
    app.run(port=5000, debug=True)
