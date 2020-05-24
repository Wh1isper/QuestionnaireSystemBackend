from tornado.testing import AsyncHTTPTestCase
from app import make_app


class BaseAsyncHTTPTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()
