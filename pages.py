import asyncio
from sanic.response import json as json_response
from sanic import Blueprint
from urllib.parse import urlparse

from db.db import db
from responses.response import Response

pages = Blueprint('pages')

#
# GET - /pages&url=:url
#
@pages.route('/pages', methods=['GET'])
async def getPageByUrl(request):
    if 'url' not in request.args:
        return json_response({ 'error': Response.BadRequest }, status=400)

    url_parser = urlparse(request.args['url'][0])
    website = url_parser.netloc
    path = url_parser.path

    page = db.findPageByWebsiteAndPath(website, path)

    # Create page.
    if page == None:
        page_id = db.insertPage(website, path)
        page = db.findPageById(page_id)

    # Get comments.
    comments = db.findCommentsByPageId(page['_id'])

    # Get users.
    users = db.findUsersByIds([comment['user_id'] for comment in comments])

    jsonComments = []
    for comment in comments:
        comment_user = None
        for user in users:
            if user['_id'] == comment['user_id']:
                comment_user = user
                break

        comment['user'] = comment_user
        jsonComments.append(comment)

    return json_response({ 'page': page, 'comments': jsonComments }, status=200)
