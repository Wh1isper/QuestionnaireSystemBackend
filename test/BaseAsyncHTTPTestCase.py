from tornado.testing import AsyncHTTPTestCase
from app import make_app
from typing import Text
import json


class BaseAsyncHTTPTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    def login(self) -> dict:
        # 登录，返回带有cookie的headers
        login_url = self.get_url(r"/api/v1/login/")
        body = {
            "email": "9573586@qq.com",
            "pwd": "password123",
            "check_code": "not test",
        }
        body = json.dumps(body)
        response = self.fetch(login_url, method='POST', body=body)
        cookie = response.headers.get("Set-Cookie")
        headers = {"Cookie": cookie}
        self.assertEqual(response.code, 200)
        return headers
