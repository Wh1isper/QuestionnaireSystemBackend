import unittest
from test.BaseAsyncHTTPTestCase import BaseAsyncHTTPTestCase
import json
import config
import time
import datetime

config.UNITTEST = True


class TestQuestionnaireCreate(BaseAsyncHTTPTestCase):
    def test_questionnaire_create(self):
        # checklist：
        #   questionnaireInfo表初始化
        #   questionnaireTemp表初始化
        #   answerRecord表初始化
        test_url = self.get_url(r"/api/v1/questionnaireCreate/")
        body = {
            "Q_title": "Q_create_test_title",
        }
        body = json.dumps(body)
        response = self.fetch(test_url, method='POST', body=body, headers=self.login())
        print(response.body)
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.body)


class TestQuestionnaireSave(BaseAsyncHTTPTestCase):
    def test_questionnaire_save(self):
        # checklist：
        #   questionnaireTemp表修改
        test_url = self.get_url(r"/api/v1/questionnaireSave/")
        body = {
            'Q_ID': 8,
            'content': [
                {
                    'question_id': 1,
                    'question_content': '问题1',
                    'question_type': 0,
                    'option': [
                        {
                            'option_id': 1,
                            'option_content': "选项1"
                        },
                        {
                            'option_id': 2,
                            'option_content': "选项2"
                        },
                    ]
                },
                {
                    'question_id': 2,
                    'question_content': '问题2',
                    'question_type': 2
                }
            ]
        }
        body = json.dumps(body)
        response = self.fetch(test_url, method='POST', body=body, headers=self.login())
        self.assertEqual(response.code, 200)


class TestQuestionnairePublish(BaseAsyncHTTPTestCase):
    def test_questionnaire_publish(self):
        # checklist：
        #   questionnaireInfo表修改：deadline字段和state字段
        #   questionnaireQuestion表新增
        #   questionnaireOption表新增
        test_url = self.get_url(r"/api/v1/questionnairePublish/")
        body = {
            "Q_ID": "8",
            "end_date": (datetime.datetime.today() + datetime.timedelta(days=15)).timestamp()
        }
        body = json.dumps(body)
        response = self.fetch(test_url, method='POST', body=body, headers=self.login())
        self.assertEqual(response.code, 200)


class TestQuestionnaireInactivate(BaseAsyncHTTPTestCase):
    def test_questionnaire_delete(self):
        # checklist
        #   questionnaireInfo表修改（state字段）
        test_url = self.get_url(r"/api/v1/questionnaireInactive/")
        body = {
            'Q_ID': 8
        }
        body = json.dumps(body)
        response = self.fetch(test_url, method='POST', body=body, headers=self.login())
        self.assertEqual(response.code, 200)


class TestQuestionnaireDelete(BaseAsyncHTTPTestCase):
    def test_questionnaire_delete(self):
        test_url = self.get_url(r"/api/v1/questionnaireDelete/")
        body = {
            'Q_ID': 2
        }
        body = json.dumps(body)
        response = self.fetch(test_url, method='POST', body=body, headers=self.login())
        self.assertEqual(response.code, 200)


class TestQuestionnaireGet(BaseAsyncHTTPTestCase):
    def test_questionnaire_get(self):
        test_url = self.get_url(r"/api/v1/questionnaireGet/?Q_ID=6")
        response = self.fetch(test_url, method='GET', headers=self.login())
        self.assertEqual(response.code, 200)
        print(response.body)


class TestQuestionnaireSubmit(BaseAsyncHTTPTestCase):
    def test_question_submit(self):
        test_url = self.get_url(r"/api/v1/questionnaireSubmit/")
        body = {
            'Q_ID': 8,
            'content': [
                {
                    'question_id': 1,
                    'question_type': 0,
                    'option': [1],
                },
                {
                    'question_id': 2,
                    'question_type': 2,
                    'content': 'test_content',
                }
            ]
        }
        body = json.dumps(body)
        response = self.fetch(test_url, method='POST', body=body)
        self.assertEqual(response.code, 200)


class TestQuestionnaireResultGet(BaseAsyncHTTPTestCase):
    def test_questionnaire_result(self):
        test_url = self.get_url(r"/api/v1/questionnaireResultGet/?Q_ID=8")
        response = self.fetch(test_url, method='GET', headers=self.login())
        print(response.body)
        self.assertEqual(response.code, 200)


class TestQuestionnaireStatistics(BaseAsyncHTTPTestCase):
    def test_questionnaire_result(self):
        test_url = self.get_url(r"/api/v1/questionnaireStatistics/?Q_ID=8")
        response = self.fetch(test_url, method='GET', headers=self.login())
        print(response.body)
        self.assertEqual(response.code, 200)


if __name__ == '__main__':
    unittest.main()
