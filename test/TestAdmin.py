# todo 分支代码覆盖
import unittest
from BaseAsyncHTTPTestCase import BaseAsyncHTTPTestCase
import json
import config

config.UNITTEST = True


class TestAdminLoginHandler(BaseAsyncHTTPTestCase):
    def test_login_success(self):
        self.admin_login()


class TestAdminChangeUserState(BaseAsyncHTTPTestCase):
    def test_ban_user(self):
        # todo 自动化验证
        test_url = self.get_url(r"/api/v1/admin/userStateChange/")
        test_body = {
            "email": "9573586@qq.com",
            "type": 1
        }
        test_body = json.dumps(test_body)
        response = self.fetch(test_url, method='POST', body=test_body, headers=self.admin_login())
        self.assertEqual(response.code, 200)

    def test_unban_user(self):
        # todo 自动化验证
        test_url = self.get_url(r"/api/v1/admin/userStateChange/")
        test_body = {
            "email": "9573586@qq.com",
            "type": 0
        }
        test_body = json.dumps(test_body)
        response = self.fetch(test_url, method='POST', body=test_body, headers=self.admin_login())
        self.assertEqual(response.code, 200)


class TestAdminChangeQuestionaireState(BaseAsyncHTTPTestCase):
    def test_ban_Questionaire(self):
        # todo 自动化验证
        test_url = self.get_url(r"/api/v1/admin/questionnaireStateChange/")
        test_body = {
            "QI_ID": 1,
            "type": 1
        }
        test_body = json.dumps(test_body)
        response = self.fetch(test_url, method='POST', body=test_body, headers=self.admin_login())
        self.assertEqual(response.code, 200)

    def test_unban_Questionaire(self):
        # todo 自动化验证
        test_url = self.get_url(r"/api/v1/admin/questionnaireStateChange/")
        test_body = {
            "QI_ID": 1,
            "type": 0
        }
        test_body = json.dumps(test_body)
        response = self.fetch(test_url, method='POST', body=test_body, headers=self.admin_login())
        self.assertEqual(response.code, 200)


class TestAdminGetUserList(BaseAsyncHTTPTestCase):
    def test_get_list(self):
        # todo 自动化验证

        test_url = self.get_url(r"/api/v1/admin/userList/")
        response = self.fetch(test_url, method='GET', headers=self.admin_login())
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.body)
        print(response.body)

        test_url = self.get_url(r"/api/v1/admin/userList/?offset={}".format(20))
        response = self.fetch(test_url, method='GET', headers=self.admin_login())
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.body)
        print(response.body)


class TestAdminGetQuestionnaireList(BaseAsyncHTTPTestCase):
    def test_get_list(self):
        # todo 自动化验证

        test_url = self.get_url(r"/api/v1/admin/questionnaireList/")
        response = self.fetch(test_url, method='GET', headers=self.admin_login())
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.body)
        print(response.body)

        test_url = self.get_url(r"/api/v1/admin/questionnaireList/?offset={}".format(20))
        response = self.fetch(test_url, method='GET', headers=self.admin_login())
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.body)
        print(response.body)


if __name__ == '__main__':
    unittest.main()
