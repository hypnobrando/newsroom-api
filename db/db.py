import json
from pymongo import MongoClient, DESCENDING
from bson import ObjectId
from datetime import datetime, date

from config.config import Config


class DB:

    def __init__(self):
        self.config = Config()
        self.db = MongoClient(self.config.dbURI)[self.config.dbName]

    # Users

    def insertUser(self, user):
        user = {
            'username': user['username'],
            'password': user['password']
        }

        return self.deserialize(self.db['users'].insert(user))

    def findUserById(self, userId):
        return self.deserialize(self.db['users'].find_one({ '_id': ObjectId(userId) }, { 'password': 0 }))

    def findUsersByIds(self, userIds):
        return self.deserialize(list(self.db['users'].find({ '_id': { '$in': [ObjectId(userId) for userId in userIds] } }, { 'password': 0 })))

    def findUserByUsernameAndPassword(self, username, password):
        return self.deserialize(self.db['users'].find_one({ 'username': username, 'password':  password}, { 'password': 0 }))

    # Pages

    def findPageById(self, pageId):
        return self.deserialize(self.db['pages'].find_one({ '_id': ObjectId(pageId) }))

    def findPageByWebsiteAndPath(self, website, path):
        return self.deserialize(self.db['pages'].find_one({ 'website': website, 'path': path }))

    def insertPage(self, website, path):
        page = {
            'website': website,
            'path': path
        }

        return self.deserialize(self.db['pages'].insert(page))

    # Comments

    def insertComment(self, user, page, message):
        comment = {
            'user_id': ObjectId(user['_id']),
            'page_id': ObjectId(page['_id']),
            'message': message,
            'timestamp': datetime.now()
        }

        return self.deserialize(self.db['comments'].insert(comment))

    def findCommentById(self, commentId):
        return self.deserialize(self.db['comments'].find_one({ '_id': ObjectId(commentId) }))

    def findCommentsByPageId(self, pageId):
        return self.deserialize(list(self.db['comments'].find({ 'page_id': ObjectId(pageId) }).sort('timestamp', DESCENDING)))

    # Helpers

    def deserialize(self, object):
        return json.loads(JSONEncoder().encode(object))


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, (datetime, date)):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


db = DB()
