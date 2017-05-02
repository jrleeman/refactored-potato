import feedparser
from flask import Flask, render_template, request

app = Flask(__name__)

rss_feeds = {'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn':'http://rss.cnn.com/rss/edition.rss',
             'fox':'http://feeds.foxnews.com/foxnews/latest',
             'onion':'http://www.theonion.com/feeds/rss'}

@app.route('/', methods=['GET', 'POST'])
def get_news():
    query = request.form.get('publication')
    if not query or query.lower() not in rss_feeds:
        publication = 'bbc'
    else:
        publication = query.lower()

    feed = feedparser.parse(rss_feeds[publication])
    return render_template('home.html',
                           articles=feed['entries'])

if __name__ == '__main__':
    app.run(port=5000, debug=True)
