import unittest
from test.BaseAsyncHTTPTestCase import BaseAsyncHTTPTestCase
import json
import config

config.UNITTEST = True


class TestQuestionnairePublish(BaseAsyncHTTPTestCase):
    pass


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
