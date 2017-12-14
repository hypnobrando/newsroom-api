from sanic import Sanic
from sanic_cors import CORS

from users import users
from comments import comments
from pages import pages
from etc import etc

app = Sanic()
app.blueprint(users)
app.blueprint(comments)
app.blueprint(pages)
app.blueprint(etc)
CORS(app)

if __name__ == "__main__":
    print('Starting up newsroom server...')
    app.run(host="0.0.0.0", port=8080)
