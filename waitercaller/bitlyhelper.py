import json
import os
from urllib.request import urlopen
from urllib.parse import quote

TOKEN = os.environ.get('BITLY_OAUTH_KEY', None)
ROOT_URL = "https://api-ssl.bitly.com"
SHORTEN = "/v3/shorten?access_token={}&longUrl={}"

class BitlyHelper:

    def shorten_url(self, longurl):
        try:
            url = ROOT_URL + SHORTEN.format(TOKEN, longurl)
            response = urlopen(url).read()
            jr = json.loads(response)
            print(jr)
            print("NEW URL CREATED", jr['data']['url'])
            return jr['data']['url']
        except Exception as e:
            print(e)
