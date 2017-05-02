import feedparser
from flask import Flask

app = Flask(__name__)

rss_feeds = {'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn':'http://rss.cnn.com/rss/edition.rss',
             'fox':'http://feeds.foxnews.com/foxnews/latest',
             'onion':'http://www.theonion.com/feeds/rss'}

@app.route('/')
@app.route('/<source>')
def get_news(source='bbc'):
    feed = feedparser.parse(rss_feeds[source])
    first_article = feed['entries'][0]
    return """<html>
    <body>
    <h1>{0} Headlines</h1>
    <b>{1}</b><br/>
    <i>{2}</i><br/>
    <p>{3}</p><br/>
    </body>
    </html>
    """.format(source,
               first_article.get('title'),
               first_article.get('published'),
               first_article.get('summary'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
