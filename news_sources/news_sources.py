import requests
from urllib.parse import urlparse, urlencode

from config.config import Config
from .src_imgs import SRC_IMGS

API_URL_EVERYTHING = 'https://newsapi.org/v2/everything'
API_URL_HEADLINES = 'https://newsapi.org/v2/top-headlines'

MAX_KEYWORDS = 10

SOURCES_ALL = ['abc-news', 'abc-news-au', 'aftenposten', 'al-jazeera-english', 'ansa', 'argaam', 'ars-technica', 'ary-news', 'associated-press', 'australian-financial-review', 'axios', 'bbc-news', 'bbc-sport', 'bild', 'blasting-news-br', 'bleacher-report', 'bloomberg', 'breitbart-news', 'business-insider', 'business-insider-uk', 'buzzfeed', 'cbc-news', 'cbs-news', 'cnbc', 'cnn', 'cnn-es', 'crypto-coins-news', 'daily-mail', 'der-tagesspiegel', 'die-zeit', 'el-mundo', 'engadget', 'entertainment-weekly', 'espn', 'espn-cric-info', 'financial-post', 'financial-times', 'focus', 'football-italia', 'fortune', 'four-four-two', 'fox-news', 'fox-sports', 'globo', 'google-news', 'google-news-ar', 'google-news-au', 'google-news-br', 'google-news-ca', 'google-news-fr', 'google-news-in', 'google-news-is', 'google-news-it', 'google-news-ru', 'google-news-sa', 'google-news-uk', 'goteborgs-posten', 'gruenderszene', 'hacker-news', 'handelsblatt', 'ign', 'il-sole-24-ore', 'independent', 'infobae', 'info-money', 'la-gaceta', 'la-nacion', 'la-repubblica', 'le-monde', 'lenta', 'lequipe', 'les-echos', 'liberation', 'marca', 'mashable', 'medical-news-today', 'metro', 'mirror', 'msnbc', 'mtv-news', 'mtv-news-uk', 'national-geographic', 'nbc-news', 'news24', 'new-scientist', 'news-com-au', 'newsweek', 'new-york-magazine', 'next-big-future', 'nfl-news', 'nhl-news', 'nrk', 'politico', 'polygon', 'rbc', 'recode', 'reddit-r-all', 'reuters', 'rt', 'rte', 'rtl-nieuws', 'sabq', 'spiegel-online', 'svenska-dagbladet', 't3n', 'talksport', 'techcrunch', 'techcrunch-cn', 'techradar', 'the-economist', 'the-globe-and-mail', 'the-guardian-au', 'the-guardian-uk', 'the-hill', 'the-hindu', 'the-huffington-post', 'the-irish-times', 'the-lad-bible', 'the-new-york-times', 'the-next-web', 'the-sport-bible', 'the-telegraph', 'the-times-of-india', 'the-verge', 'the-wall-street-journal', 'the-washington-post', 'time', 'usa-today', 'vice-news', 'wired', 'wired-de', 'wirtschafts-woche', 'xinhua-net', 'ynet']

SOURCES_FILTERED = ['abc-news', 'abc-news-au', 'associated-press', 'australian-financial-review', 'axios', 'bbc-news', 'bbc-sport', 'bleacher-report', 'bloomberg', 'breitbart-news', 'business-insider', 'business-insider-uk', 'buzzfeed', 'cbc-news', 'cbs-news', 'cnbc', 'cnn', 'cnn-es', 'crypto-coins-news', 'daily-mail', 'engadget', 'entertainment-weekly', 'espn', 'espn-cric-info', 'financial-post', 'financial-times', 'focus', 'fortune', 'four-four-two', 'fox-news', 'fox-sports', 'hacker-news', 'ign', 'independent', 'liberation', 'marca', 'mashable', 'medical-news-today', 'metro', 'mirror', 'msnbc', 'mtv-news', 'mtv-news-uk', 'national-geographic', 'nbc-news', 'new-scientist', 'news-com-au', 'newsweek', 'new-york-magazine', 'next-big-future', 'nfl-news', 'nhl-news', 'politico', 'polygon', 'rbc', 'recode', 'reuters', 'talksport', 'techcrunch', 'techcrunch-cn', 'techradar', 'the-economist', 'the-globe-and-mail', 'the-guardian-au', 'the-guardian-uk', 'the-hill', 'the-huffington-post', 'the-irish-times', 'the-lad-bible', 'the-new-york-times', 'the-next-web', 'the-sport-bible', 'the-telegraph', 'the-verge', 'the-wall-street-journal', 'the-washington-post', 'time', 'usa-today', 'vice-news', 'wired', 'wired-de']

SOURCE_STRING = ','.join(SOURCES_FILTERED)

TOP_SOURCES = ['abc-news', 'bbc-news', 'bloomberg', 'cbc-news', 'cbs-news', 'cnbc', 'cnn', 'cnn-es', 'daily-mail', 'fox-news', 'ign', 'msnbc', 'national-geographic', 'nbc-news', 'politico', 'reuters', 'techcrunch', 'the-economist', 'the-huffington-post', 'the-new-york-times', 'the-wall-street-journal', 'the-washington-post', 'time', 'usa-today']

TOP_SOURCE_STRING = ','.join(TOP_SOURCES)

class NewsSources:
    def __init__(self):
        self.config = Config()

    def getRelated(self, keywords, site):
        headers = { 'X-Api-Key': self.config.newsAPIKey }
        q = ''
        nKeywordsToUse = MAX_KEYWORDS if len(keywords) >= MAX_KEYWORDS else len(keywords)
        nKeyWords = 0
        iterator = 0
        SEPARATOR = ' OR '
        while iterator < len(keywords) and nKeyWords < MAX_KEYWORDS:
            iterator+=1
            keyword = keywords[nKeyWords]
            if len(keyword) < 3:
                continue

            q += keyword + SEPARATOR
            nKeyWords+=1

        q = q[:len(q)-len(SEPARATOR)]

        r = requests.get(API_URL_EVERYTHING+'?'+urlencode({'q':q, 'sortBy': 'relevancy', 'language': 'en', 'sources': SOURCE_STRING}), headers=headers)
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
                if website == site:
                    continue

                sources.add(article['source']['name'])

                related.append({
                    'title': article['title'],
                    'url': article['url'],
                    'website': article['source']['name'],
                    'img_url': article['urlToImage'],
                    'published_at': article['publishedAt']
                })

        return related

    def getHeadlines(self):
        headers = { 'X-Api-Key': self.config.newsAPIKey }
        r = requests.get(API_URL_HEADLINES + '?'+urlencode({'sources': TOP_SOURCE_STRING, 'pageSize': 100}), headers=headers)
        resp = r.json()

        headlines = []
        if 'articles' in resp:
            sources = set()
            for i in range(len(resp['articles'])):
                if len(sources) == 3:
                    break

                article = resp['articles'][i]

                if article['source']['name'] in sources:
                    continue

                sources.add(article['source']['name'])

                headlines.append({
                    'title': article['title'],
                    'url': article['url'],
                    'website': article['source']['name'],
                    'img_url': article['urlToImage'],
                    'published_at': article['publishedAt']
                })

        return headlines

    def getSrcImg(host):
        if host not in SRC_IMGS:
            return None
        return SRC_IMGS[host]
