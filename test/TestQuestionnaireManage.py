import unittest
from test.BaseAsyncHTTPTestCase import BaseAsyncHTTPTestCase
import json
import config
import time
import datetime

config.UNITTEST = True


class TestQuestionnaireCreate(BaseAsyncHTTPTestCase):
    def test_questionnaire_create(self):
        test_url = self.get_url(r"/api/v1/questionnaireCreate/")
        body = {
            "Q_title": "Q_create_test_title",
        }
        body = json.dumps(body)
        response = self.fetch(test_url, method='POST', body=body, headers=self.login())
        print(response.body)
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.body)


class TestQuestionnairePublish(BaseAsyncHTTPTestCase):
    def test_questionnaire_publish(self):
        test_url = self.get_url(r"/api/v1/questionnairePublish/")
        body = {
            "Q_ID": "2",
            "end_date": (datetime.datetime.today() + datetime.timedelta(days=15)).timestamp()
        }
        body = json.dumps(body)
        response = self.fetch(test_url, method='POST', body=body, headers=self.login())
        self.assertEqual(response.code, 200)


class TestQuestionSave(BaseAsyncHTTPTestCase):
    pass


class TestQuestionnaireDelete(BaseAsyncHTTPTestCase):
    pass


class TestQuestionnaireInactivate(BaseAsyncHTTPTestCase):
    pass


class TestQuestionnaireGet(BaseAsyncHTTPTestCase):
    pass


class TestQuestionnaireSubmit(BaseAsyncHTTPTestCase):
    pass


class TestQuestionnaireResultGet(BaseAsyncHTTPTestCase):
    pass


class TestQuestionnaireStatistics(BaseAsyncHTTPTestCase):
    pass


if __name__ == '__main__':
    unittest.main()
