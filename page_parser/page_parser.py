from urllib.parse import urlparse, urlencode
from newspaper import Article
from datetime import datetime

from news_sources.news_sources import NewsSources

class PageParser:
    def __init__(self, url):
        if 'http://' != url[:len('http://')] and 'https://' != url[:len('https://')]:
            url = 'https://' + url

        url_parser = urlparse(url)
        self.url = url
        self.website = url_parser.netloc
        self.path = url_parser.path
        self.cleanURL()
        self.parser = Article(self.url)
        self.news = NewsSources()

    def cleanURL(self):
        if 'http://' == self.website[:len('http://')]:
            self.website = self.website[len('http://'):]
        elif 'https://' == self.website[:len('https://')]:
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

        # Get html for iframe if we need it.
        html = None

        related = self.news.getRelated(self.parser.keywords, self.website)

        return {
            'website': self.website,
            'path': self.path,
            'authors': self.parser.authors,
            'title': self.parser.title,
            'keywords': self.parser.keywords,
            'html': html,
            'related': related,
            'timestamp': datetime.now()
        }
