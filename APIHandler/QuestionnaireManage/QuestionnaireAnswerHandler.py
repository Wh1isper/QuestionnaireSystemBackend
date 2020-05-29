from BaseHandler import BaseHandler


class QuestionnaireSubmit(BaseHandler):
    # todo 问卷提交
    pass


class QuestionnaireResult(BaseHandler):
    # todo 问卷结果拉取（全量）
    pass


class QuestionnaireStatistics(BaseHandler):
    # todo 问卷结果统计
    pass


from config import *

default_handlers = [
    (r"/api/v1/questionnaireSubmit/", QuestionnaireSubmit),
    (r"/api/v1/questionnaireResultGet/", QuestionnaireResult),
    (r"/api/v1/questionnaireStatistics/", QuestionnaireStatistics)
]
