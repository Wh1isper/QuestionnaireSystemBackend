# todo 分支代码覆盖
import unittest
from test.BaseAsyncHTTPTestCase import BaseAsyncHTTPTestCase
import json
import config

config.UNITTEST = True


class TestAdminLoginHandler(BaseAsyncHTTPTestCase):
    def test_login_success(self):
        test_url = self.get_url(r'/api/v1/admin/login/')
        body = {
            "admin": config.ADMIN_ACOUNT,
            "pwd": 'password12345'
        }
        body = json.dumps(body)
        response = self.fetch(test_url, method='POST', body=body)
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.headers.get('Set-cookie'))


class TestAdminChangeUserState(BaseAsyncHTTPTestCase):
    def test_ban_user(self):
        # todo 自动化验证
        login_url = self.get_url(r'/api/v1/admin/login/')
        body = {
            "admin": config.ADMIN_ACOUNT,
            "pwd": 'password12345'
        }
        body = json.dumps(body)
        response = self.fetch(login_url, method='POST', body=body)
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.headers.get('Set-cookie'))
        cookie = response.headers.get("Set-Cookie")
        headers = {"Cookie": cookie}
        test_url = self.get_url(r"/api/v1/admin/userStateChange/")
        test_body = {
            "email": "9573586@qq.com",
            "type": 1
        }
        response = self.fetch(test_url, method='POST', body=test_body, headers=headers)
        self.assertEqual(response.code, 200)

    def test_unban_user(self):
        # todo 自动化验证
        login_url = self.get_url(r'/api/v1/admin/login/')
        body = {
            "admin": config.ADMIN_ACOUNT,
            "pwd": 'password12345'
        }
        body = json.dumps(body)
        response = self.fetch(login_url, method='POST', body=body)
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.headers.get('Set-cookie'))
        cookie = response.headers.get("Set-Cookie")
        headers = {"Cookie": cookie}
        test_url = self.get_url(r"/api/v1/admin/userStateChange/")
        test_body = {
            "email": "9573586@qq.com",
            "type": 0
        }
        response = self.fetch(test_url, method='POST', body=test_body, headers=headers)
        self.assertEqual(response.code, 200)


class TestAdminChangeQuestionaireState(BaseAsyncHTTPTestCase):
    def test_ban_Questionaire(self):
        # todo 自动化验证
        login_url = self.get_url(r'/api/v1/admin/login/')
        body = {
            "admin": config.ADMIN_ACOUNT,
            "pwd": 'password12345'
        }
        body = json.dumps(body)
        response = self.fetch(login_url, method='POST', body=body)
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.headers.get('Set-cookie'))
        cookie = response.headers.get("Set-Cookie")
        headers = {"Cookie": cookie}
        test_url = self.get_url(r"/api/v1/admin/questionnaireStateChange/")
        test_body = {
            "Q_ID": "9573586@qq.com",
            "type": 1
        }
        response = self.fetch(test_url, method='POST', body=test_body, headers=headers)
        self.assertEqual(response.code, 200)

    def test_unban_Questionaire(self):
        # todo 自动化验证
        login_url = self.get_url(r'/api/v1/admin/login/')
        body = {
            "admin": config.ADMIN_ACOUNT,
            "pwd": 'password12345'
        }
        body = json.dumps(body)
        response = self.fetch(login_url, method='POST', body=body)
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.headers.get('Set-cookie'))
        cookie = response.headers.get("Set-Cookie")
        headers = {"Cookie": cookie}
        test_url = self.get_url(r"/api/v1/admin/questionnaireStateChange/")
        test_body = {
            "Q_ID": "9573586@qq.com",
            "type": 0
        }
        response = self.fetch(test_url, method='POST', body=test_body, headers=headers)
        self.assertEqual(response.code, 200)


class TestAdminGetUserList(BaseAsyncHTTPTestCase):
    def test_get_list(self):
        # todo 自动化验证
        login_url = self.get_url(r'/api/v1/admin/login/')
        body = {
            "admin": config.ADMIN_ACOUNT,
            "pwd": 'password12345'
        }
        body = json.dumps(body)
        response = self.fetch(login_url, method='POST', body=body)
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.headers.get('Set-cookie'))
        cookie = response.headers.get("Set-Cookie")
        headers = {"Cookie": cookie}
        test_url = self.get_url(r"/api/v1/admin/userList/")
        response = self.fetch(test_url, method='GET', headers=headers)
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.body)
        print(response.body)

        test_url = self.get_url(r"/api/v1/admin/userList/?offset={}".format(20))
        response = self.fetch(test_url, method='GET', headers=headers)
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.body)
        print(response.body)


class TestAdminGetQuestionnaireList(BaseAsyncHTTPTestCase):
    def test_get_list(self):
        # todo 自动化验证
        login_url = self.get_url(r'/api/v1/admin/login/')
        body = {
            "admin": config.ADMIN_ACOUNT,
            "pwd": 'password12345'
        }
        body = json.dumps(body)
        response = self.fetch(login_url, method='POST', body=body)
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.headers.get('Set-cookie'))
        cookie = response.headers.get("Set-Cookie")
        headers = {"Cookie": cookie}
        test_url = self.get_url(r"/api/v1/admin/questionnaireList/")
        response = self.fetch(test_url, method='GET', headers=headers)
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.body)
        print(response.body)

        test_url = self.get_url(r"/api/v1/admin/questionnaireList/?offset={}".format(20))
        response = self.fetch(test_url, method='GET', headers=headers)
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.body)
        print(response.body)


if __name__ == '__main__':
    unittest.main()
