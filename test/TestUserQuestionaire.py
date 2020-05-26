import unittest
from test.BaseAsyncHTTPTestCase import BaseAsyncHTTPTestCase
import json
import config

config.DEBUG = True


class TestUserGetQuestionnaireList(BaseAsyncHTTPTestCase):
    def test_get_list(self):
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

        test_url = self.get_url(r"/api/v1/userQuestionnaireList/")
        response = self.fetch(test_url, method='GET', headers=headers)
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.body)
        print(response.body)


class TestQuestionnaireRename(BaseAsyncHTTPTestCase):
    def test_get_list(self):
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

        test_url = self.get_url(r"/api/v1/questionnaireRename/")
        test_body = {
            "Q_ID": 1,
            "Q_Name": "rename_test"
        }
        test_body = json.dumps(test_body)
        response = self.fetch(test_url, method='POST', body=test_body, headers=headers)
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.body)
        print(response.body)


if __name__ == '__main__':
    unittest.main()
