import asyncio
from sanic.response import json as json_response
from sanic import Blueprint

etc = Blueprint('etc')

@etc.route('/healthcheck', methods=['GET'])
async def healthcheck(request):
    return json_response({ 'success': 'booyah' }, status=200)
