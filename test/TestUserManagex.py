import unittest
from test.BaseAsyncHTTPTestCase import BaseAsyncHTTPTestCase
import json
import config

config.DEBUG = True


class TestUserRegister(BaseAsyncHTTPTestCase):
    # todo 用户注册流程
    def test_register(self):
        pass


class TestUserLogin(BaseAsyncHTTPTestCase):
    # todo 用户登录流程
    def test_user_login(self):
        pass


class TestUserLogout(BaseAsyncHTTPTestCase):
    # todo 用户注销流程
    def test_user_logout(self):
        pass


class TestUserInfoModify(BaseAsyncHTTPTestCase):
    # todo 用户信息修改
    def test_user_info_modify(self):
        pass


if __name__ == '__main__':
    unittest.main()
