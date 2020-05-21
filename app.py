import sys
sys.path.append('./source')
sys.path.append('/APIHandler')
sys.path.append('./ORM')

import tornado.ioloop
import tornado.web

from CheckcodeHandler import CheckcodeHandler
from LoginHandler import LoginHandler

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # 向响应中添加数据
        # self.write('hello,tornado,my name is get...')
        self.render('index.html')


def make_app():
    settings = {
        "cookie_secret": "this is not a secret cookie",
        "xsrf_cookies": False,
    }
    PWD_SAULT = "this is not a password sault"
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/api/v1/checkCode/", CheckcodeHandler),
        (r"/api/v1/login/",LoginHandler,dict(pwd_sault=PWD_SAULT))
    ],
        **settings,
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
