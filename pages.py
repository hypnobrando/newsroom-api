import asyncio
from sanic.response import json as json_response
from sanic.response import html as html_response
from sanic import Blueprint
from page_parser.page_parser import PageParser

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

    page_parser = PageParser(request.args['url'][0])
    website = page_parser.website
    path = page_parser.path

    page = db.findPageByWebsiteAndPath(website, path)

    # Create page.
    if page == None:
        parsed = page_parser.getPage()
        if not parsed:
            return json_response({ 'error': Response.BadRequest }, status=400)

        page_id = db.insertPage(parsed)
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


#
# GET - /pages/:page_id/html
#
@pages.route('/pages/<page_id>/html', methods=['GET'])
async def getPageHTML(request, page_id):
    page = db.findPageById(page_id)
    if page == None:
        return html_response(Response.NotFoundError, status=404)

    return html_response(page['html'], status=200)
