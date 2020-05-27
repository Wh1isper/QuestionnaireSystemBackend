from BaseHandler import BaseHandler


class QuestionnairePublishHandler(BaseHandler):
    pass


class QuestionnaireDeleteHandler(BaseHandler):
    pass


class QuestionnaireInactiveHandler(BaseHandler):
    pass


from config import *

default_handlers = [
    (r"/api/v1/questionnairePublish/", QuestionnairePublishHandler),
    (r"/api/v1/questionnaireDelete/", QuestionnaireDeleteHandler),
    (r"/api/v1/questionnaireInactive/", QuestionnaireInactiveHandler),
]
