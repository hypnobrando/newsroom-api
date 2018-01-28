import os

class Config:

    def __init__(self):
        self.env = 'development' if self.isDev(self.getEnvVar('ENV')) else self.getEnvVar('ENV')
        self.dbURI = 'mongodb://localhost:27017/' if self.isDev(self.env) else self.getEnvVar('DB_URI')
        self.dbName = 'newsroom'

        self.fbClientId = self.getEnvVar('FB_CLIENT_ID') if self.isProd() else '164677740818802'
        self.fbClientSecret = self.getEnvVar('FB_CLIENT_SECRET') if self.isProd() else 'fec2bf57efdb838b1b1f4209552557b6'
        self.fbRedirectURI =  ('https://api.newsroom.bep-projects.com' if self.isProd() else 'http://localhost:8080') + '/users/facebook_login'

        self.newsAPIKey = '33098d6865144874b8baa9aaaade964f'

    def getEnvVar(self, key):
        if key in os.environ:
            return os.environ[key]
        return None

    def isDev(self, var):
        return var != 'testing' and var != 'production'

    def isTesting(self):
        return self.env == 'testing'

    def isProd(self):
        return self.env == 'production'
