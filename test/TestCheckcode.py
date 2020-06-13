# todo 分支代码覆盖
import unittest
from test.BaseAsyncHTTPTestCase import BaseAsyncHTTPTestCase
import json
import config
config.UNITTEST = True


class TestCheckcodeHandler(BaseAsyncHTTPTestCase):
    def test_get_checkcode(self):
        test_url = self.get_url('/api/v1/checkCode/')
        response = self.fetch(test_url, method='GET')
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.headers.get('Set-cookie'))
        self.assertIsNotNone(response.body)


class TestEmailCheckcodeHandler(BaseAsyncHTTPTestCase):
    def test_get_email_checkcode(self):
        test_url = self.get_url('/api/v1/emailCode/')
        body = {
            "email": "9573586@qq.com"
        }
        body = json.dumps(body)
        response = self.fetch(test_url, method='POST', body=body)
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.headers.get('Set-cookie'))
        self.assertIsNotNone(response.body)


if __name__ == '__main__':
    unittest.main()
