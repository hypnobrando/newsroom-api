import asyncio
from sanic.response import json as json_response
from sanic import Blueprint

from db.db import db
from responses.response import Response

users = Blueprint('users')

#
# POST - /users
# {
#   username: string,
#   password: string
# }
#
@users.route('/users', methods=['POST'])
async def postUser(request):
    body = request.json

    if 'username' not in body or 'password' not in body:
        return json_response({ 'error': Response.BadRequest }, status=400)

    user = db.findByUsername(body['username'])
    if user != None:
        return json_response({ 'error': Response.BadRequest }, status=400)

    user_id = db.insertUser(body)
    user = db.findUserById(user_id)

    return json_response({ 'user': user }, status=201)

#
# GET - /users/:user_id
#
@users.route('/users/<user_id>', methods=['GET'])
async def getUser(request, user_id):
    user = db.findUserById(user_id)
    if user == None:
        return json_response({ 'error': Response.NotFoundError }, status=404)

    return json_response({ 'user': user }, status=200)


#
# GET - /users/login?username=:username&password=:password
#
@users.route('/users/login', methods=['GET'])
async def getUserByUsernameAndPassword(request):
    if 'username' not in request.args or 'password' not in request.args:
        return json_response({ 'error': Response.BadRequest }, status=400)

    user = db.findUserByUsernameAndPassword(request.args['username'][0], request.args['password'][0])
    if user == None:
        return json_response({ 'error': Response.NotFoundError }, status=404)

    return json_response({ 'user': user }, status=200)
