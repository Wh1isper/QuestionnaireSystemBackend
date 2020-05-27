from BaseHandler import BaseHandler


class QuestionnaireSave(BaseHandler):
    pass


class QuestionnaireContent(BaseHandler):
    pass


from config import *

default_handlers = [
    (r"/api/v1/questionnaireSave/", QuestionnaireSave),
    (r"/api/v1/questionnaireGet/", QuestionnaireContent),
]
