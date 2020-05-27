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

    # log info
    print("...Creating Route")

    handlers = [(r'/', test_hanler), ]
    handlers.extend(load_handlers('APIHandler.CheckcodeHandler'))
    handlers.extend(load_handlers('APIHandler.UserManage.LoginHandler'))
    handlers.extend(load_handlers('APIHandler.UserManage.RegisterHandler'))
    handlers.extend(load_handlers('APIHandler.UserManage.UserInfoHandler'))
    handlers.extend(load_handlers('APIHandler.UserQuestionnaire.UserQuestionnaireHandler'))
    handlers.extend(load_handlers('APIHandler.UserQuestionnaire.QuestionnaireRenameHandler'))
    handlers.extend(load_handlers('APIHandler.Admin.AdminLoginHandler'))
    handlers.extend(load_handlers('APIHandler.Admin.AdminManageHandler'))
    handlers.extend(load_handlers('APIHandler.QuestionnaireManage.QuestionnaireAnswerHandler'))
    handlers.extend(load_handlers('APIHandler.QuestionnaireManage.QuestionnaireContentHandler'))
    handlers.extend(load_handlers('APIHandler.QuestionnaireManage.QuestionnaireStateHandler'))

    # log info
    for handler in handlers:
        url = handler[0]
        handler_class = handler[1]
        print(url, handler_class)

    return tornado.web.Application(handlers, **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(PORT)

    # log info
    print("servers running at 127.0.0.1:{}".format(PORT))

    tornado.ioloop.IOLoop.current().start()
