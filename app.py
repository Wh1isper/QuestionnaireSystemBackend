import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello world")


def make_app():
    settings = {
        "cookie_secret": "this is not a secret cookie",
        "xsrf_cookies": False,
    }

    return tornado.web.Application([
        (r"/", MainHandler),
    ],
        **settings,
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
