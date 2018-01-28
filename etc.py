import asyncio
from sanic.response import json as json_response
from sanic import Blueprint

from news_sources.news_sources import NewsSources

etc = Blueprint('etc')

@etc.route('/healthcheck', methods=['GET'])
async def healthcheck(request):
    return json_response({ 'success': 'BOOYAH' }, status=200)

@etc.route('/headlines', methods=['GET'])
async def headlines(request):
    news = NewsSources()

    headlines = news.getHeadlines()

    return json_response({ 'headlines': headlines }, status=200)
