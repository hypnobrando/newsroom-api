import asyncio
from sanic.response import json as json_response
from sanic.response import html, raw
from sanic import Blueprint
import requests
import json

from db.db import db
from config.config import Config
from responses.response import Response

users = Blueprint('users')
config = Config()

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

@users.route('/users/facebook_login', methods=['GET'])
async def facebookUserLogin(request):
    if 'code' not in request.args:
        return json_response({ 'error': Response.BadRequest }, status=400)

    code = request.args['code'][0]

    fbookURL = 'https://graph.facebook.com/oauth/access_token? \
        client_id=' + config.fbClientId + \
        '&redirect_uri=' + config.fbRedirectURI + \
        '&client_secret=' + config.fbClientSecret + \
        '&code=' + code

    r = requests.get(fbookURL)
    fbInfo = r.json()
    if 'access_token' not in fbInfo:
        return html('<h2 style="color:white;">' + json.dumps({ 'error': fbInfo }) + '</h2>')

    r = requests.get("https://graph.facebook.com/me?fields=id,first_name,last_name,picture&access_token=" + fbInfo['access_token'])
    fbUser = r.json()
    if 'id' not in fbUser:
        return html('<h2 style="color:white;">' + json.dumps({ 'error': fbUser }) + '</h2>')

    user = db.findByFBID(fbUser['id'])
    user_id = None
    if user != None:
        db.updateUser(user['_id'], { 'first_name': fbUser['first_name'], 'last_name': fbUser['last_name'], 'fb_id': fbUser['id'], 'prof_pic': fbUser['picture']['data']['url'] })
        user_id = user['_id']
    else:
        user_id = db.insertUser({ 'first_name': fbUser['first_name'], 'last_name': fbUser['last_name'], 'fb_id': fbUser['id'], 'prof_pic': fbUser['picture']['data']['url'] })

    user = db.findUserById(user_id)
    resp = '<h1 id="user" style="color:white;">' + json.dumps(user) + '</h1>'

    return html(resp)

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
