import sys

sys.path.append('./source')
sys.path.append('./APIHandler')
sys.path.append('./ORM')

import tornado.ioloop
import tornado.web
from config import *


def load_handlers(name):
    """Load the (URL pattern, handler) tuples for each component."""
    mod = __import__(name, fromlist=['default_handlers'])
    return mod.default_handlers


class test_hanler(tornado.web.RequestHandler):
    def get(self):
        self.write(str([{"Q_ID": "1"}]))


def make_app():
    settings = {
        "cookie_secret": COOKIE_SECRET,
        "xsrf_cookies": False,
    }
    handlers = [(r'/', test_hanler), ]
    handlers.extend(load_handlers('APIHandler.CheckcodeHandler'))
    handlers.extend(load_handlers('APIHandler.UserManage.LoginHandler'))
    handlers.extend(load_handlers('APIHandler.UserManage.RegisterHandler'))
    handlers.extend(load_handlers('APIHandler.UserManage.UserInfoHandler'))
    return tornado.web.Application(handlers, **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
