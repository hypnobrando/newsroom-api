from urllib.parse import urlparse, urlencode
from newspaper import Article
from datetime import datetime
import requests

API_KEY = '33098d6865144874b8baa9aaaade964f'
API_URL = 'https://newsapi.org/v2/everything'
MAX_KEYWORDS = 6

class PageParser:
    def __init__(self, url):
        if '?' in url:
            url = url[:url.index('?')]
        if '#' in url:
            url = url[:url.index('#')]

        if 'http://' != url[:len('http://')] and 'https://' != url[:len('https://')]:
            url = 'http://' + url

        url_parser = urlparse(url)
        self.url = url
        self.website = url_parser.netloc
        self.path = url_parser.path
        self.cleanURL()
        self.parser = Article(self.url)

    def cleanURL(self):
        if 'http://' == self.website[:len('http://')]:
            self.url = self.url
            self.website = self.website[len('http://'):]
        elif 'https://' == self.website[:len('https://')]:
            self.url = self.url
            self.website = self.website[len('https://'):]

        if self.website != '' and '/' == self.website[-1]:
            self.website = self.website[:-1]

        if self.path == '' or self.path[-1] != '/':
            self.path += '/'

    def loadParser(self):
        try:
            self.parser.download()
            self.parser.parse()
            self.parser.nlp()
            return True
        except:
            return False

    def getPage(self):
        # returns the dict representation of the page
        if not self.loadParser():
            return None

        # query for related api
        headers = { 'X-Api-Key': API_KEY }
        q = ''
        nKeywordsToUse = MAX_KEYWORDS if len(self.parser.keywords) >= MAX_KEYWORDS else len(self.parser.keywords)
        nKeyWords = 0
        iterator = 0
        SEPARATOR = ' OR '
        while iterator < len(self.parser.keywords) and nKeyWords < MAX_KEYWORDS:
            iterator+=1
            keyword = self.parser.keywords[nKeyWords]
            if len(keyword) < 3:
                continue

            q += keyword + SEPARATOR
            nKeyWords+=1

        q = q[:len(q)-len(SEPARATOR)]

        r = requests.get(API_URL+'?'+urlencode({'q':q, 'sortBy': 'relevancy', 'language': 'en'}), headers=headers)
        resp = r.json()

        related = []
        sources = set()
        for i in range(len(resp['articles'])):
            article = resp['articles'][i]

            if article['source']['name'] in sources:
                continue

            url_parser = urlparse(article['url'])
            website = url_parser.netloc
            if website == self.website:
                continue

            sources.add(article['source']['name'])

            related.append({
                'title': article['title'],
                'url': article['url'],
                'website': article['source']['name'],
                'img_url': article['urlToImage'],
                'published_at': article['publishedAt']
            })

        return {
            'website': self.website,
            'path': self.path,
            'authors': self.parser.authors,
            'title': self.parser.title,
            'keywords': self.parser.keywords,
            'related': related,
            'timestamp': datetime.now()
        }
