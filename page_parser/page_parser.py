from urllib.parse import urlparse, urlencode
from newspaper import Article
from datetime import datetime
import requests

API_KEY = '33098d6865144874b8baa9aaaade964f'
API_URL = 'https://newsapi.org/v2/everything'
MAX_KEYWORDS = 10

SOURCES_ALL = ['abc-news', 'abc-news-au', 'aftenposten', 'al-jazeera-english', 'ansa', 'argaam', 'ars-technica', 'ary-news', 'associated-press', 'australian-financial-review', 'axios', 'bbc-news', 'bbc-sport', 'bild', 'blasting-news-br', 'bleacher-report', 'bloomberg', 'breitbart-news', 'business-insider', 'business-insider-uk', 'buzzfeed', 'cbc-news', 'cbs-news', 'cnbc', 'cnn', 'cnn-es', 'crypto-coins-news', 'daily-mail', 'der-tagesspiegel', 'die-zeit', 'el-mundo', 'engadget', 'entertainment-weekly', 'espn', 'espn-cric-info', 'financial-post', 'financial-times', 'focus', 'football-italia', 'fortune', 'four-four-two', 'fox-news', 'fox-sports', 'globo', 'google-news', 'google-news-ar', 'google-news-au', 'google-news-br', 'google-news-ca', 'google-news-fr', 'google-news-in', 'google-news-is', 'google-news-it', 'google-news-ru', 'google-news-sa', 'google-news-uk', 'goteborgs-posten', 'gruenderszene', 'hacker-news', 'handelsblatt', 'ign', 'il-sole-24-ore', 'independent', 'infobae', 'info-money', 'la-gaceta', 'la-nacion', 'la-repubblica', 'le-monde', 'lenta', 'lequipe', 'les-echos', 'liberation', 'marca', 'mashable', 'medical-news-today', 'metro', 'mirror', 'msnbc', 'mtv-news', 'mtv-news-uk', 'national-geographic', 'nbc-news', 'news24', 'new-scientist', 'news-com-au', 'newsweek', 'new-york-magazine', 'next-big-future', 'nfl-news', 'nhl-news', 'nrk', 'politico', 'polygon', 'rbc', 'recode', 'reddit-r-all', 'reuters', 'rt', 'rte', 'rtl-nieuws', 'sabq', 'spiegel-online', 'svenska-dagbladet', 't3n', 'talksport', 'techcrunch', 'techcrunch-cn', 'techradar', 'the-economist', 'the-globe-and-mail', 'the-guardian-au', 'the-guardian-uk', 'the-hill', 'the-hindu', 'the-huffington-post', 'the-irish-times', 'the-lad-bible', 'the-new-york-times', 'the-next-web', 'the-sport-bible', 'the-telegraph', 'the-times-of-india', 'the-verge', 'the-wall-street-journal', 'the-washington-post', 'time', 'usa-today', 'vice-news', 'wired', 'wired-de', 'wirtschafts-woche', 'xinhua-net', 'ynet']

SOURCES_FILTERED = ['abc-news', 'abc-news-au', 'associated-press', 'australian-financial-review', 'axios', 'bbc-news', 'bbc-sport', 'blasting-news-br', 'bleacher-report', 'bloomberg', 'breitbart-news', 'business-insider', 'business-insider-uk', 'buzzfeed', 'cbc-news', 'cbs-news', 'cnbc', 'cnn', 'cnn-es', 'crypto-coins-news', 'daily-mail', 'engadget', 'entertainment-weekly', 'espn', 'espn-cric-info', 'financial-post', 'financial-times', 'focus', 'football-italia', 'fortune', 'four-four-two', 'fox-news', 'fox-sports', 'hacker-news', 'ign', 'independent', 'info-money', 'la-nacion', 'la-repubblica', 'le-monde', 'lenta', 'lequipe', 'les-echos', 'liberation', 'marca', 'mashable', 'medical-news-today', 'metro', 'mirror', 'msnbc', 'mtv-news', 'mtv-news-uk', 'national-geographic', 'nbc-news', 'new-scientist', 'news-com-au', 'newsweek', 'new-york-magazine', 'next-big-future', 'nfl-news', 'nhl-news', 'nrk', 'politico', 'polygon', 'rbc', 'recode', 'reuters', 't3n', 'talksport', 'techcrunch', 'techcrunch-cn', 'techradar', 'the-economist', 'the-globe-and-mail', 'the-guardian-au', 'the-guardian-uk', 'the-hill', 'the-huffington-post', 'the-irish-times', 'the-lad-bible', 'the-new-york-times', 'the-next-web', 'the-sport-bible', 'the-telegraph', 'the-verge', 'the-wall-street-journal', 'the-washington-post', 'time', 'usa-today', 'vice-news', 'wired', 'wired-de']

SOURCE_STRING = ','.join(SOURCES_FILTERED)

class PageParser:
    def __init__(self, url):
        '''
        if '?' in url:
            url = url[:url.index('?')]
        if '#' in url:
            url = url[:url.index('#')]
        '''

        if 'http://' != url[:len('http://')] and 'https://' != url[:len('https://')]:
            url = 'https://' + url

        url_parser = urlparse(url)
        self.url = url
        self.website = url_parser.netloc
        self.path = url_parser.path
        self.cleanURL()
        self.parser = Article(self.url)

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

        '''
        r = requests.get(self.url)
        frame_ancestors = None
        if 'content-security-policy' in r.headers:
            for elem in r.headers['content-security-policy'].split(';'):
                if 'frame-ancestors' in elem:
                    frame_ancestors = elem

            if frame_ancestors:
                html = self.parser.html
        if 'X-Frame-Options' in r.headers:
            html = self.parser.html
        '''

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

        r = requests.get(API_URL+'?'+urlencode({'q':q, 'sortBy': 'relevancy', 'language': 'en', 'sources': SOURCE_STRING}), headers=headers)
        resp = r.json()

        related = []

        if 'articles' in resp:
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
            'html': html,
            'related': related,
            'timestamp': datetime.now()
        }
