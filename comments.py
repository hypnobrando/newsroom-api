import asyncio
from sanic.response import json as json_response
from sanic import Blueprint

from db.db import db
from responses.response import Response

comments = Blueprint('comments')

#
# POST - /users/:user_id/pages/:page_id/comments
# {
#   message: string
# }
#
@comments.route('/users/<user_id>/pages/<page_id>/comments', methods=['POST'])
async def postComment(request, user_id, page_id):
    body = request.json
    if 'message' not in body:
        return json_response({ 'error': Response.BadRequest }, status=400)

    user = db.findUserById(user_id)
    if user == None:
        return json_response({ 'error': Response.BadRequest }, status=400)

    page = db.findPageById(page_id)
    if page == None:
        return json_response({ 'error': Response.BadRequest }, status=400)

    comment_id = db.insertComment(user, page, body['message'])
    comment = db.findCommentById(comment_id)

    return json_response({ 'comment': comment }, status=201)
