import sys

sys.path.append('../source')
sys.path.append('../APIHandler')
sys.path.append('../APIHandler/Admin')
sys.path.append('../APIHandler/QuestionnaireManage')
sys.path.append('../APIHandler/UserManage')
sys.path.append('../APIHandler/UserQuestionnaire')
sys.path.append('../ORM')
sys.path.append('..')

from tornado.testing import AsyncHTTPTestCase
from app import *
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

    def login_other_acount(self):
        login_url = self.get_url(r"/api/v1/login/")
        body = {
            "email": "testemail@qq.com",
            "pwd": "password123",
            "check_code": "not test",
        }
        body = json.dumps(body)
        response = self.fetch(login_url, method='POST', body=body)
        cookie = response.headers.get("Set-Cookie")
        headers = {"Cookie": cookie}
        self.assertEqual(response.code, 200)
        return headers

    def admin_login(self) -> dict:
        login_url = self.get_url(r'/api/v1/admin/login/')
        body = {
            "admin": "admin",
            "pwd": 'password12345'
        }
        body = json.dumps(body)
        response = self.fetch(login_url, method='POST', body=body)
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.headers.get('Set-cookie'))
        cookie = response.headers.get("Set-Cookie")
        headers = {"Cookie": cookie}
        return headers
