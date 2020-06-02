# todo 分支代码覆盖、自动化验证
import unittest
from test.BaseAsyncHTTPTestCase import BaseAsyncHTTPTestCase
import json
import config
import time

config.UNITTEST = True


class TestUserRegister(BaseAsyncHTTPTestCase):
    # 用户注册流程 目前需要手动进入数据库查看测试结果
    # todo 自动化验证注册数据并清理
    def test_register(self):
        test_url = self.get_url(r'/api/v1/register/')
        body = {
            "email": "testemail@qq.com",
            "usrname": "jizsss",
            "birth": time.time(),
            "pwd": "password123",
            "email_code": "not test",
            "sex": 0
        }
        body = json.dumps(body)
        response = self.fetch(test_url, method='POST', body=body)
        print(response.body)
        self.assertEqual(response.code, 200)


class TestUserLogin(BaseAsyncHTTPTestCase):
    # 用户登录流程
    def test_user_login(self):
        test_url = self.get_url(r"/api/v1/login/")
        body = {
            "email": "9573586@qq.com",
            "pwd": "password123",
            "check_code": "not test",
        }
        body = json.dumps(body)
        response = self.fetch(test_url, method='POST', body=body)
        print(response.headers.get("Set-cookie"))
        self.assertEqual(response.code, 200)


class TestUserLogout(BaseAsyncHTTPTestCase):
    # 用户注销流程
    def test_user_logout(self):
        login_url = self.get_url(r"/api/v1/login/")
        body = {
            "email": "9573586@qq.com",
            "pwd": "password123",
            "check_code": "not test",
        }
        body = json.dumps(body)
        response = self.fetch(login_url, method='POST', body=body)
        print("login")
        print(response.headers.get("Set-cookie"))
        self.assertEqual(response.code, 200)

        test_url = self.get_url(r"/api/v1/logout/")
        print("logout")
        response = self.fetch(test_url, method='GET')
        print(response.headers.get("Set-cookie"))
        self.assertEqual(response.code, 200)


class TestUserInfoModify(BaseAsyncHTTPTestCase):
    # 用户信息获取 目前需要手动进入数据库查看测试结果
    # todo 自动化验证返回数据并清理
    def test_get_user_info(self):
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

        test_url = self.get_url(r"/api/v1/userInfo/")
        response = self.fetch(test_url, method='GET', headers=headers)
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.body)
        print(response.body)

    # 用户信息修改 目前需要手动进入数据库查看测试结果
    # todo 自动化验证返回数据并清理
    def test_user_info_modify(self):
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

        test_url = self.get_url(r"/api/v1/userInfo/")
        body = {
            "usrname": "jizs-modify",
            "birth": time.time(),
            "sex": 0,
        }
        body = json.dumps(body)
        response = self.fetch(test_url, method='POST', body=body, headers=headers)
        self.assertEqual(response.code, 200)


class TestUserPwdChange(BaseAsyncHTTPTestCase):
    # 用户密码修改 目前需要手动进入数据库查看测试结果
    # todo 自动化验证返回数据并清理
    def test_user_info_modify(self):
        login_url = self.get_url(r"/api/v1/login/")
        body = {
            "email": "9573586@qq.com",
            "pwd": "password12345",
            "check_code": "not test",
        }
        body = json.dumps(body)
        response = self.fetch(login_url, method='POST', body=body)
        cookie = response.headers.get("Set-Cookie")
        headers = {"Cookie": cookie}
        self.assertEqual(response.code, 200)

        test_url = self.get_url(r"/api/v1/changePwd/")
        body = {
            "old_pwd": "password12345",
            "pwd": "password123"
        }
        body = json.dumps(body)
        response = self.fetch(test_url, method='POST', body=body, headers=headers)
        self.assertEqual(response.code, 200)


if __name__ == '__main__':
    unittest.main()
