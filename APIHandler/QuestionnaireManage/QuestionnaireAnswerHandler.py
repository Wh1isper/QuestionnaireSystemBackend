from BaseHandler import BaseHandler


class QuestionnaireSubmit(BaseHandler):
    pass


class QuestionnaireResult(BaseHandler):
    pass


class QuestionnaireStatistics(BaseHandler):
    pass


from config import *

default_handlers = [
    (r"/api/v1/questionnaireSubmit/", QuestionnaireSubmit),
    (r"/api/v1/questionnaireResultGet/", QuestionnaireResult),
    (r"/api/v1/questionnaireStatistics/", QuestionnaireStatistics)
]
